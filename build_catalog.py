"""Construye catalogo_productos.json: producto -> {grupo, subgrupo, sub_subgrupo}.

Se corre A MANO, una sola vez (o cuando cambie el catálogo/menú de productos)
-- NO en cada extracción diaria de main.py. Recorre los nodos hoja de
catalog.LEAF_NODES (~128) filtrando el reporte por frGrupos[]=<id>, pero
sobre TODO el rango histórico de una sola vez (una consulta por categoría,
no una por día), y guarda a qué categoría pertenece cada producto visto.

Un mismo producto puede aparecer bajo más de una categoría (combos, ítems
compartidos, recategorizaciones). Para esos casos se cuenta cuántas filas de
venta tuvo el producto bajo cada categoría y se queda con la de más votos
(no la última consultada); el detalle completo de cada conflicto queda en
catalogo_conflictos.json para revisión manual.

Uso:
    python build_catalog.py
    python build_catalog.py --start 2025-01-01 --end 2026-08-09
"""
import argparse
import json
import time
import urllib.parse
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from config import DATUM_BASE_URL, AREAS, STATIC_PARAMS
from catalog import LEAF_NODES
from scraper import login, extract_from_table

OUTPUT_FILE = Path("catalogo_productos.json")
CONFLICTS_FILE = Path("catalogo_conflictos.json")

MAX_RETRIES = 3
RETRY_DELAY = 5.0


def _build_url(node_id, start, end):
    start_enc = urllib.parse.quote(start.strftime("%d/%m/%Y"), safe='')
    end_enc = urllib.parse.quote(end.strftime("%d/%m/%Y"), safe='')
    area_query = "&".join(f"frArea[]={a['id']}" for a in AREAS)

    return (
        f"{DATUM_BASE_URL}/venta_reporte_productos.php?"
        f"{STATIC_PARAMS}&{area_query}&frInicio={start_enc}&frFinal={end_enc}"
        f"&frGrupos[]={node_id}"
    )


def _get_with_retries(session, url):
    """GET con reintentos ante errores transitorios de conexión (evita que
    un nodo entero quede sin categorizar por un timeout/desconexión)."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=120)
            response.raise_for_status()
            return response
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                print(f" reintento {attempt}/{MAX_RETRIES - 1} ({e})...", end="")
                time.sleep(RETRY_DELAY)
    raise last_error


def build_catalog(session, start, end, delay=1.0):
    # producto (lowercase) -> Counter({entry_key: cantidad de filas vistas})
    votes = defaultdict(Counter)
    # entry_key (tupla hasheable) -> dict {grupo, subgrupo, sub_subgrupo} y nombre original
    entries_by_key = {}
    originals = {}  # producto (lowercase) -> forma original (con mayúsculas) más reciente
    failed_nodes = []

    for i, node in enumerate(LEAF_NODES, start=1):
        tag = " > ".join(p for p in (node["grupo"], node["subgrupo"], node["sub_subgrupo"]) if p) \
            or node["name"]
        print(f"[{i}/{len(LEAF_NODES)}] {tag}", end="...")

        url = _build_url(node["id"], start, end)
        try:
            response = _get_with_retries(session, url)
        except Exception as e:
            print(f"ERROR: {e}")
            failed_nodes.append(tag)
            continue

        records = extract_from_table(response.text)
        counts = Counter(r["producto"].strip() for r in records if r.get("producto"))

        entry = {"grupo": node["grupo"], "subgrupo": node["subgrupo"],
                  "sub_subgrupo": node["sub_subgrupo"]}
        entry_key = (entry["grupo"], entry["subgrupo"], entry["sub_subgrupo"])
        entries_by_key[entry_key] = entry

        for producto, count in counts.items():
            key = producto.lower()
            votes[key][entry_key] += count
            originals[key] = producto

        print(f"{len(counts)} productos")
        if delay:
            time.sleep(delay)

    catalog = {}
    conflicts = {}
    for key, counter in votes.items():
        winner_key, winner_votes = counter.most_common(1)[0]
        catalog[key] = entries_by_key[winner_key]
        if len(counter) > 1:
            conflicts[key] = {
                "producto": originals[key],
                "elegido": entries_by_key[winner_key],
                "opciones": [
                    {"categoria": entries_by_key[k], "filas": v}
                    for k, v in counter.most_common()
                ],
            }

    if conflicts:
        print(f"\n{len(conflicts)} productos aparecieron en más de una categoría "
              f"(se quedó con la de más filas de venta; detalle en {CONFLICTS_FILE}).")
        with open(CONFLICTS_FILE, "w", encoding="utf-8") as f:
            json.dump(conflicts, f, ensure_ascii=False, indent=2)

    if failed_nodes:
        print(f"\n{len(failed_nodes)} categorías fallaron tras {MAX_RETRIES} intentos: "
              f"{', '.join(failed_nodes)}")
        print("Volvé a correr el script para completarlas (no se perdió lo demás).")

    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=date.fromisoformat, default=date(2025, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat,
                         default=date.today() - timedelta(days=1))
    args = parser.parse_args()

    session = login()
    if not session:
        return

    print(f"Construyendo catálogo de {args.start.isoformat()} a {args.end.isoformat()} "
          f"({len(LEAF_NODES)} categorías, una consulta por categoría, no por día)...")

    catalog = build_catalog(session, args.start, args.end)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"\nCatálogo guardado: {OUTPUT_FILE} ({len(catalog)} productos)")


if __name__ == "__main__":
    main()
