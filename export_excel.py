"""Genera un Excel formateado a partir de ventas.jsonl (rápido, para archivos grandes)."""
import json
import sys
from pathlib import Path

import pandas as pd

# Límite de Excel es 1,048,576 filas por hoja; dejamos margen.
MAX_ROWS = 1_000_000

COLUMNS = ["date", "area", "grupo", "subgrupo", "sub_subgrupo", "tipo", "producto",
           "cantidad", "precio", "impuesto", "total", "costo", "margen", "utilidad"]
HEADERS = {
    "date": "Fecha", "area": "Área",
    "grupo": "Grupo", "subgrupo": "Subgrupo", "sub_subgrupo": "Sub-subgrupo",
    "tipo": "Tipo", "producto": "Producto",
    "cantidad": "Cantidad", "precio": "Precio", "impuesto": "Impuesto",
    "total": "Total", "costo": "Costo", "margen": "Margen", "utilidad": "Utilidad",
}
WIDTHS = {"Fecha": 12, "Área": 26, "Grupo": 20, "Subgrupo": 22,
          "Sub-subgrupo": 24, "Tipo": 28, "Producto": 34}
MONEY_COLS = {"Precio", "Impuesto", "Total", "Costo", "Margen", "Utilidad"}
MONEY_FMT = '$#,##0.00;[Red]-$#,##0.00'


def load_records(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def json_to_excel(jsonl_path, xlsx_path=None):
    jsonl_path = Path(jsonl_path)
    if xlsx_path is None:
        xlsx_path = jsonl_path.with_suffix(".xlsx")
    xlsx_path = Path(xlsx_path)

    df = pd.DataFrame(load_records(jsonl_path))
    if df.empty:
        print("El jsonl está vacío; no se generó Excel.")
        return 0, None

    for c in COLUMNS:
        if c not in df.columns:
            df[c] = None
    df = df[COLUMNS]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values(
        ["date", "area", "grupo", "subgrupo", "sub_subgrupo", "tipo", "producto"]
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