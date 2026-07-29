from config import AREA_MAP, PROTECTED_AREAS

import json
from pathlib import Path

def resolve_area(tipo, current_area) :
    if current_area in PROTECTED_AREAS:
        return current_area
    if not tipo:
        return current_area
    t = tipo.strip()
    if "descuento" in t.lower():
        return current_area

    for prefix, area in AREA_MAP.items():
        if t == prefix or t.startswith(prefix + " "):
            return area

    return current_area

def normalize_records(records):
    for r in records:
        r["area"] = resolve_area(r.get("tipo"), r.get("area"))

    return records

def normalize_file(path):
    path = Path(path)
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    normalize_records(records)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    return len(records)