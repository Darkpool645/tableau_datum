import json
from pathlib import Path

from scraper import (
    login, combinationsPerMonth, getData,
    scrape_combinations, retry_failures,
    combinationsPerDay
)

TEST_MODE = False
OUTPUT_FILE = Path("ventas.jsonl")
FAILURES_FILE = Path("fallidas.json")


def reset_outputs(*paths):
    for p in paths:
        if p.exists():
            p.unlink()
            print(f"Limpiado: {p}")


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    reset_outputs(OUTPUT_FILE, FAILURES_FILE)

    session = login()
    if not session:
        return
    # combinations = getData(session, combinationsPerMonth())
    combinations = getData(session, combinationsPerDay())
    records, failures = scrape_combinations(
        session, combinations, limit=1 if TEST_MODE else None
    )

    if failures:
        recovered, failures = retry_failures(session, failures)
        records.extend(recovered)
        print(f"Recuperados en reintentos: {len(recovered)} registros")

    write_jsonl(OUTPUT_FILE, records)

    total = len(combinations) if not TEST_MODE else 1
    completadas = total - len(failures)
    print(f"\nCobertura: {completadas}/{total} combinaciones "
          f"({completadas / total * 100:.1f}%)")
    print(f"Total: {len(records)} registros")

    if failures:
        with open(FAILURES_FILE, "w", encoding="utf-8") as f:
            json.dump(failures, f, ensure_ascii=False, indent=2)
        print(f"Quedaron {len(failures)} sin recuperar → {FAILURES_FILE}")


if __name__ == "__main__":
    main()