"""Genera un Excel formateado a partir de ventas.jsonl (rápido, para archivos grandes)."""
import json
import re
import sys
from pathlib import Path

import pandas as pd

# Límite de Excel es 1,048,576 filas por hoja; dejamos margen.
MAX_ROWS = 1_000_000

# Catálogo producto -> {grupo, subgrupo, sub_subgrupo}, generado una sola vez
# (o cuando cambie el menú) con build_catalog.py. Si no existe, esas tres
# columnas quedan vacías; no bloquea la generación del Excel.
CATALOG_FILE = Path(__file__).with_name("catalogo_productos.json")
CATALOG_FIELDS = ["grupo", "subgrupo", "sub_subgrupo"]

COLUMNS = ["date", "area", "grupo", "subgrupo", "sub_subgrupo", "tipo", "subtipo", "producto",
           "cantidad", "precio", "impuesto", "total", "costo", "margen", "utilidad"]
HEADERS = {
    "date": "Fecha", "area": "Área",
    "grupo": "Grupo", "subgrupo": "Subgrupo", "sub_subgrupo": "Sub-subgrupo",
    "tipo": "Tipo", "subtipo": "Subtipo", "producto": "Producto",
    "cantidad": "Cantidad", "precio": "Precio", "impuesto": "Impuesto",
    "total": "Total", "costo": "Costo", "margen": "Margen", "utilidad": "Utilidad",
}
WIDTHS = {"Fecha": 12, "Área": 26, "Grupo": 20, "Subgrupo": 20, "Sub-subgrupo": 20,
          "Tipo": 24, "Subtipo": 16, "Producto": 34}
MONEY_COLS = {"Precio", "Impuesto", "Total", "Costo", "Margen", "Utilidad"}
MONEY_FMT = '$#,##0.00;[Red]-$#,##0.00'

# --- Separación de "Tipo" en "Tipo" + "Subtipo" -----------------------------
# El scraper guarda cosas como "Carrito 1 Bebidas con alcohol",
# "Mulligan Bebidas sin alcohol" o "Vista Alimentos". Aquí:
#   - Si termina en "Bebidas con alcohol" / "Bebidas sin alcohol":
#       tipo    -> "<Área> Bebidas"
#       subtipo -> "Con alcohol" / "Sin alcohol"
#   - Cualquier otro valor (Alimentos, Descuentos, Green Fees, Proshop,
#     Tabaco, Renta Carrito, etc.) se deja igual y subtipo queda vacío.
TIPO_SUBTIPO_PATTERN = re.compile(
    r'^(.*\bBebidas)\s+(con alcohol|sin alcohol)$', re.IGNORECASE
)


def split_tipo_subtipo(tipo):
    if tipo is None or (isinstance(tipo, float) and pd.isna(tipo)):
        return tipo, None
    m = TIPO_SUBTIPO_PATTERN.match(str(tipo).strip())
    if m:
        return m.group(1).strip(), m.group(2).strip().capitalize()
    return tipo, None
# -----------------------------------------------------------------------------


def load_records(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_catalog(path=CATALOG_FILE):
    """Carga catalogo_productos.json (producto en minúsculas -> categoría).
    Si no existe, devuelve {} y las columnas de categoría quedan vacías."""
    path = Path(path)
    if not path.exists():
        print(f"Aviso: no se encontró {path}; Grupo/Subgrupo/Sub-subgrupo "
              f"quedarán vacíos. Corre build_catalog.py para generarlo.")
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def json_to_excel(jsonl_path, xlsx_path=None):
    jsonl_path = Path(jsonl_path)
    if xlsx_path is None:
        xlsx_path = jsonl_path.with_suffix(".xlsx")
    xlsx_path = Path(xlsx_path)

    df = pd.DataFrame(load_records(jsonl_path))
    if df.empty:
        print("El jsonl está vacío; no se generó Excel.")
        return 0, None

    # Aseguramos que exista la columna "tipo" antes de separarla.
    if "tipo" not in df.columns:
        df["tipo"] = None

    # Separación Tipo -> Tipo + Subtipo (no afecta al jsonl original, solo al export)
    split_result = df["tipo"].apply(split_tipo_subtipo)
    df["tipo"] = split_result.apply(lambda x: x[0])
    df["subtipo"] = split_result.apply(lambda x: x[1])

    # Grupo/Subgrupo/Sub-subgrupo: join local por producto contra el catálogo
    # cacheado (build_catalog.py), no vuelve a consultar DATUM.
    catalog = load_catalog()
    if "producto" not in df.columns:
        df["producto"] = None
    keys = df["producto"].fillna("").astype(str).str.strip().str.lower()
    for field in CATALOG_FIELDS:
        df[field] = keys.map(lambda k: catalog.get(k, {}).get(field))

    for c in COLUMNS:
        if c not in df.columns:
            df[c] = None
    df = df[COLUMNS]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values(
        ["date", "area", "tipo", "subtipo", "producto"]
    ).reset_index(drop=True)

    chunks = [df.iloc[i:i + MAX_ROWS] for i in range(0, len(df), MAX_ROWS)]

    with pd.ExcelWriter(xlsx_path, engine="xlsxwriter",
                        datetime_format="yyyy-mm-dd") as writer:
        wb = writer.book
        header_fmt = wb.add_format({
            "font_name": "Arial", "bold": True, "font_size": 11,
            "font_color": "FFFFFF", "bg_color": "1F4E78",
            "align": "center", "valign": "vcenter", "border": 1,
        })
        base = {"font_name": "Arial", "font_size": 10}
        fmt_text = wb.add_format(base)
        fmt_date = wb.add_format({**base, "num_format": "yyyy-mm-dd"})
        fmt_int = wb.add_format({**base, "num_format": "#,##0"})
        fmt_money = wb.add_format({**base, "num_format": MONEY_FMT})

        for idx, chunk in enumerate(chunks, start=1):
            sheet = "Ventas" if len(chunks) == 1 else f"Ventas {idx}"
            out = chunk.rename(columns=HEADERS)
            out.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]

            # encabezado con formato
            for col, name in enumerate(out.columns):
                ws.write(0, col, name, header_fmt)

            # formato por columna entera (O(1) por columna, no por celda)
            for col, name in enumerate(out.columns):
                if name == "Fecha":
                    fmt = fmt_date
                elif name == "Cantidad":
                    fmt = fmt_int
                elif name in MONEY_COLS:
                    fmt = fmt_money
                else:
                    fmt = fmt_text
                ws.set_column(col, col, WIDTHS.get(name, 13), fmt)

            ws.freeze_panes(1, 0)
            ws.autofilter(0, 0, len(out), len(out.columns) - 1)

    return len(df), xlsx_path


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "ventas.jsonl"
    dst = sys.argv[2] if len(sys.argv) > 2 else None
    n, path = json_to_excel(src, dst)
    if path:
        print(f"Excel generado: {path}  ({n} registros)")