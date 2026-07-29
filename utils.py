from config import FIELDS, NUM_COLS, NUMERIC

def to_number(value):
    if value is None:
        return None

    clean = value.strip().replace(",","").replace("%","").replace("$","")
    if clean in ("", "-"):
        return None

    try:
        return float(clean)
    except ValueError:
        return None


def is_clean_row(row) :
    if len(row) < NUM_COLS:
        return False

    if row[0].strip().lower() in ("total", "totales", "area", "área", ""):
        return False

    return to_number(row[3]) is not None

def row_to_dict(row):
    register = dict(zip(FIELDS, row[:NUM_COLS]))
    for field in NUMERIC:
        register[field] = to_number(register[field])

    return register