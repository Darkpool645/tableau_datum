import json
from pathlib import Path
from datetime import date, timedelta

from scraper import (
    login, getData, scrape_combinations,
    retry_failures, combinationsPerDay
)
from postprocess import normalize_file
from export_excel import json_to_excel

TEST_MODE = False
OUTPUT_FILE = Path("ventas.jsonl")
FAILURES_FILE = Path("fallidas.json")


def reset_outputs(*paths):
    for p in paths:
        if p.exists():
            p.unlink()
            print(f"Limpiado: {p}")


def last_covered_date(path):
    """Fecha más reciente ya guardada en el jsonl, o None si no existe/está vacío."""
    if not path.exists() or path.stat().st_size == 0:
        return None
    latest = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line).get("date")
            except json.JSONDecodeError:
                continue
            if d:
                d = date.fromisoformat(d)
                if latest is None or d > latest:
                    latest = d
    return latest


def append_jsonl(path, records):
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def finalize():
    """Normaliza áreas y genera el Excel. Se ejecuta haya o no datos nuevos."""
    if not OUTPUT_FILE.exists():
        return
    total, cambios = normalize_file(OUTPUT_FILE)
    print(f"Limpieza: {cambios}/{total} registros reasignados por área.")
    n, path = json_to_excel(OUTPUT_FILE)
    if path:
        print(f"Excel generado: {path} ({n} registros)")


def main():
    session = login()
    if not session:
        return

    yesterday = date.today() - timedelta(days=1)

    last = last_covered_date(OUTPUT_FILE)
    if last is None:
        start = date(2025, 1, 1)
        print("No hay ventas.jsonl previo → extracción completa desde 2025-01-01.")
    else:
        start = last + timedelta(days=1)
        print(f"Último día cubierto: {last.isoformat()}")

    if start > yesterday:
        print(f"Ya está actualizado hasta {yesterday.isoformat()}. Nada que extraer.")
        finalize()
        return

    print(f"Extrayendo del {start.isoformat()} al {yesterday.isoformat()}")

    # Solo reiniciamos el archivo de fallidas; el de ventas se conserva y se apenda.
    reset_outputs(FAILURES_FILE)

    combinations = getData(session, combinationsPerDay(start, yesterday))
    records, failures = scrape_combinations(
        session, combinations, limit=1 if TEST_MODE else None
    )

    if failures:
        recovered, failures = retry_failures(session, failures)
        records.extend(recovered)
        print(f"Recuperados en reintentos: {len(recovered)} registros")

    append_jsonl(OUTPUT_FILE, records)

    total_combos = len(combinations) if not TEST_MODE else 1
    completadas = total_combos - len(failures)
    print(f"\nCobertura: {completadas}/{total_combos} combinaciones "
          f"({completadas / total_combos * 100:.1f}%)")
    print(f"Nuevos registros añadidos: {len(records)}")

    if failures:
        with open(FAILURES_FILE, "w", encoding="utf-8") as f:
            json.dump(failures, f, ensure_ascii=False, indent=2)
        print(f"Quedaron {len(failures)} sin recuperar → {FAILURES_FILE}")

    finalize()


if __name__ == "__main__":
    main()