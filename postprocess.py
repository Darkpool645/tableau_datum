from config import AREA_MAP, PROTECTED_AREAS, GROUP_FIELDS

import json
from pathlib import Path
import shutil


def _depth(record):
    """Profundidad de la ruta jerárquica de un registro (0..3)."""
    return sum(1 for f in GROUP_FIELDS if record.get(f))


def dedupe_deepest(records):
    """Solo relevante con QUERY_STRATEGY='all_nodes': un mismo producto puede
    aparecer al consultar el grupo padre y también el hijo. Se conserva la
    aparición con la etiqueta MÁS profunda por (date, area, tipo, producto).
    Con 'leaves' no hay duplicados y esta función es un no-op."""
    best = {}
    for r in records:
        key = (r.get("date"), r.get("area"), r.get("tipo"), r.get("producto"))
        if key not in best or _depth(r) > _depth(best[key]):
            best[key] = r
    return list(best.values())

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
        r["area"] = resolve_area(r.get("tipo"), antes)
        if r["area"] != antes:
            cambios += 1

    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    return len(records), cambios