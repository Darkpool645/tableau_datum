import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar
import urllib.parse
import time
from datetime import date, timedelta

from config import (
    DATUM_USER, DATUM_PASSWORD, DATUM_BASE_URL, AREAS, STATIC_PARAMS
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


def month_chunks(start, end):
    """Divide [start, end] en tramos mensuales (recortados al rango real).
    Sirve para procesar y persistir la extracción mes por mes sin perder el
    detalle diario: dentro de cada tramo se sigue consultando día por día,
    porque el reporte de DATUM agrega todo el rango pedido en una sola fila
    por área/producto/tipo (no trae fecha por fila)."""
    chunks = []
    current = date(start.year, start.month, 1)
    while current <= end:
        last_day = calendar.monthrange(current.year, current.month)[1]
        month_end = date(current.year, current.month, last_day)
        chunks.append((max(start, current), min(end, month_end)))
        current = date(current.year + 1, 1, 1) if current.month == 12 \
            else date(current.year, current.month + 1, 1)

    return chunks


def _build_url(combo):
    """Arma la URL del reporte para un combo (día/áreas)."""
    start_enc = urllib.parse.quote(combo["startDay"], safe='')
    final_enc = urllib.parse.quote(combo["endDay"], safe='')

    area_ids = combo.get("areaIds") or [combo["areaId"]]
    area_query = "&".join([f"frArea[]={aid}" for aid in area_ids])

    return (
        f"{DATUM_BASE_URL}/venta_reporte_productos.php?"
        f"{STATIC_PARAMS}&{area_query}&frInicio={start_enc}&frFinal={final_enc}"
    )


def getData(session, date_combinations):
    """Adjunta la URL completa a cada combo (día × todas las áreas)."""
    if not session:
        print("No hay una sesion activa. Abortando getData")
        return

    for combo in date_combinations:
        combo["fullUrl"] = _build_url(combo)

    return date_combinations


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
        tag = f"{combo['date']} | {combo.get('areaName', '')}"
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

        # Etiquetamos cada fila con su fecha.
        for r in records:
            r["date"] = combo["date"]

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