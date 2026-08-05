import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar
import urllib.parse
import time
from datetime import date, timedelta

from config import (
    DATUM_USER, DATUM_PASSWORD, DATUM_BASE_URL, AREAS,
    STATIC_PARAMS, query_nodes, GROUP_FIELDS
)
from utils import is_clean_row, row_to_dict


def login():
    session = requests.Session()
    form_payload = {
        'frUsuario': DATUM_USER,
        'frContrasena': DATUM_PASSWORD,
        'frAccion': "Ingresar",
        "frCompleto": ""
    }

    try:
        response = session.post(DATUM_BASE_URL, data=form_payload)
        response.raise_for_status()

        if not session.cookies.get('PHPSESSID'):
            print("Advertencia: El login fue exitoso, pero no se recibio PHPSESSID.")

        return session

    except requests.exceptions.RequestException as e:
        print(f"Error al intentar iniciar sesion: {e}")
        return None


def combinationsPerMonth():
    today = date.today()
    start_year = 2025
    end_year = today.year
    combinations = []

    for year in range(start_year, end_year + 1):
        max_month = today.month if year == end_year else 12

        for month in range(1, max_month + 1):
            start_day = f"01/{month:02d}/{year}"

            if year == end_year and month == max_month:
                last_day = today.day
            else:
                last_day = calendar.monthrange(year, month)[1]

            end_day = f"{last_day:02d}/{month:02d}/{year}"

            for area in AREAS:
                combinations.append({
                    "areaId": area["id"],
                    "areaName": area["name"],
                    "startDay": start_day,
                    "endDay": end_day
                })

    return combinations


def _build_url(combo, node_id):
    """Arma la URL del reporte para un combo (día/áreas) filtrando por un
    único nodo de la jerarquía en frGrupos[]."""
    start_enc = urllib.parse.quote(combo["startDay"], safe='')
    final_enc = urllib.parse.quote(combo["endDay"], safe='')

    area_ids = combo.get("areaIds") or [combo["areaId"]]
    area_query = "&".join([f"frArea[]={aid}" for aid in area_ids])

    # Antes: frGrupos[] llevaba TODA la lista. Ahora lleva UN nodo por consulta,
    # así cada fila devuelta pertenece a ese grupo/subgrupo/sub-subgrupo.
    groups_query = f"frGrupos[]={node_id}"

    return (
        f"{DATUM_BASE_URL}/venta_reporte_productos.php?"
        f"{STATIC_PARAMS}&{area_query}&frInicio={start_enc}&frFinal={final_enc}&{groups_query}"
    )


def getData(session, date_combinations):
    """Expande cada combo (día × todas las áreas) en un combo por NODO de la
    jerarquía. A cada combo resultante se le adjunta:
        - node_id
        - grupo / subgrupo / sub_subgrupo  (para etiquetar las filas)
        - fullUrl

    Si un combo ya trae 'node_id' (caso de reintento), solo se le reconstruye
    la URL sin volver a expandir.
    """
    if not session:
        print("No hay una sesion activa. Abortando getData")
        return

    nodes = query_nodes()
    expanded = []

    for combo in date_combinations:
        # --- Reintento: el combo ya está a nivel de nodo ---
        if "node_id" in combo:
            combo["fullUrl"] = _build_url(combo, combo["node_id"])
            expanded.append(combo)
            continue

        # --- Expansión normal: un combo por nodo ---
        for node in nodes:
            child = dict(combo)
            child["node_id"] = node["id"]
            child["grupo"] = node["grupo"]
            child["subgrupo"] = node["subgrupo"]
            child["sub_subgrupo"] = node["sub_subgrupo"]
            child["nodeName"] = node["name"]
            child["fullUrl"] = _build_url(child, node["id"])
            expanded.append(child)

    print(f"Iniciando extraccion: {len(date_combinations)} días × "
          f"{len(nodes)} nodos = {len(expanded)} consultas.")

    return expanded


def extract_from_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    table_results = None
    for table in soup.find_all('table'):
        if 'Promedio de tiempos' in table.text and 'Margen' in table.text:
            table_results = table
            break

    if not table_results:
        print('No se encontro la tabla de resultados en el HTML')
        return []

    records = []
    for row in table_results.find_all('tr'):
        columns = row.find_all('td')
        if not columns:
            continue
        row_texts = [col.get_text(strip=True) for col in columns]
        if is_clean_row(row_texts):
            records.append(row_to_dict(row_texts))

    return records


def scrape_combinations(session, combinations, limit=None, delay=1.0):
    target = combinations[:limit] if limit else combinations
    all_records = []
    failures = []

    for i, combo in enumerate(target, start=1):
        tag = (f"{combo.get('nodeName', combo['node_id'])} "
               f"[{combo.get('grupo','')}] | {combo['startDay']}")
        print(f"[{i}/{len(target)}] {tag}", end="...")

        try:
            response = session.get(combo["fullUrl"], timeout=120)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: {e}")
            failures.append({**{k: v for k, v in combo.items() if k != "fullUrl"},
                             "error": str(e)})
            continue

        records = extract_from_table(response.text)

        # Etiquetamos cada fila con su fecha y su ruta en la jerarquía.
        for r in records:
            r["date"] = combo["date"]
            for f in GROUP_FIELDS:
                r[f] = combo.get(f, "")

        all_records.extend(records)
        print(f"{len(records)} registros")

        if delay:
            time.sleep(delay)

    if failures:
        print(f"\n{len(failures)} consultas fallaron.")

    return all_records, failures


def retry_failures(session, failures, max_rounds=3, base_delay=5.0):
    recovered = []
    pending = failures

    for round_num in range(1, max_rounds + 1):
        if not pending:
            break

        wait = base_delay * (2 ** (round_num - 1))
        print(f'\n--- Reintento {round_num}/{max_rounds}: '
              f'{len(pending)} pendientes (esperando {wait:.0f}s) ---')

        time.sleep(wait)

        combos = [{k: v for k, v in f.items() if k != "error"} for f in pending]
        combos = getData(session, combos)

        records, pending = scrape_combinations(session, combos, delay=2.0)
        recovered.extend(records)

    return recovered, pending


def combinationsPerDay(start=None, end=None):
    if start is None:
        start = date(2025, 1, 1)
    if end is None:
        end = date.today() - timedelta(days=1)

    area_ids = [a["id"] for a in AREAS]
    combinations = []
    current = start
    while current <= end:
        day_str = current.strftime("%d/%m/%Y")
        iso = current.isoformat()

        combinations.append({
            "areaIds": area_ids,            # <-- lista completa, clave PLURAL
            "areaName": "Todas las áreas",  # solo para el log
            "startDay": day_str,
            "endDay": day_str,
            "date": iso
        })

        current += timedelta(days=1)

    return combinations