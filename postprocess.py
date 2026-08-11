from config import AREA_MAP, DISCOUNT_AREA_MAP, PROTECTED_AREAS

import json
from pathlib import Path
import shutil


def resolve_area(tipo, current_area, producto=None):
    if current_area in PROTECTED_AREAS:
        return current_area
    if not tipo:
        return current_area
    t = tipo.strip()
    if "descuento" in t.lower():
        if producto:
            area = DISCOUNT_AREA_MAP.get(producto.strip().lower())
            if area:
                return area
        return current_area

    for prefix, area in AREA_MAP.items():
        if t == prefix or t.startswith(prefix + " "):
            return area

    return current_area

def normalize_records(records):
    for r in records:
        r["area"] = resolve_area(r.get("tipo"), r.get("area"), r.get("producto"))

    return records

def normalize_file(path, backup=True):
    """Reasigna áreas sobre un .jsonl existente, reescribiéndolo en el sitio.

    Devuelve (total_registros, registros_reasignados).
    """
    path = Path(path)
    if not path.exists():
        print(f"No existe {path}")
        return 0, 0

    if backup:
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))

    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    cambios = 0
    for r in records:
        antes = r.get("area")
        r["area"] = resolve_area(r.get("tipo"), antes, r.get("producto"))
        if r["area"] != antes:
            cambios += 1

    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    return len(records), cambios