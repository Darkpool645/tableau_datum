"""Jerarquía de categorías de producto (grupo -> subgrupo -> sub-subgrupo).

Solo la usa build_catalog.py. No forma parte del flujo diario de scraping:
DATUM únicamente revela a qué categoría pertenece una fila si filtras el
reporte por esa categoría (frGrupos[]=<id>), así que en vez de repetir esa
consulta cada día (día × nodo), build_catalog.py recorre los nodos hoja UNA
sola vez sobre todo el histórico y cachea el resultado producto -> categoría
en catalogo_productos.json.
"""

HIERARCHY = [
    { "id": 32, "name": "***"},
    { "id": 68, "name": "****"},
    { "id": 9, "name": "BARRA", "children": [
        { "id": 11, "name": "Bebidas Frías" },
        { "id": 10, "name": "Cafés" },
        { "id": 13, "name": "Cervezas" },
        { "id": 12, "name": "Cockteles" },
        { "id": 7, "name": "Jugos", "children": [
            { "id": 139, "name": "Los especiales" },
            { "id": 138, "name": "Sub recetas jugos" },
        ]},
        { "id": 15, "name": "Licores", "children": [
            { "id": 88, "name": "Aperitivos" },
            { "id": 87, "name": "Brandy & Cognac" },
            { "id": 89, "name": "Ginebra y Vodka" },
            { "id": 92, "name": "Mezcal" },
            { "id": 91, "name": "Ron" },
            { "id": 93, "name": "Tequila" },
            { "id": 90, "name": "Whisky" },
        ]},
        { "id": 102, "name": "Mezcladores Barra" },
        { "id": 96, "name": "Te's" },
        { "id": 14, "name": "Vinos", "children": [
            { "id": 95, "name": "Blancos/Rosados/Espumosos" },
            { "id": 94, "name": "Tintos" },
        ]},
    ]},
    { "id": 130, "name": "CALLOS CORTES", "children": [
        { "id": 131, "name": "Marisquería", "children": [
            { "id": 133, "name": "A elegir" },
            { "id": 134, "name": "Ceviches" },
            { "id": 137, "name": "Mariscadas" },
            { "id": 135, "name": "Tacos" },
            { "id": 136, "name": "Tostadas" },
        ]},
        { "id": 132, "name": "Sub recetas callos" },
    ]},
    { "id": 140, "name": "CAMPO DE GOLF", "children": [
        { "id": 142, "name": "Accesorios", "children": [
            { "id": 178, "name": "Bloqueador" },
            { "id": 57, "name": "Cinturones" },
            { "id": 176, "name": "Encendedor" },
            { "id": 177, "name": "Gel" },
            { "id": 144, "name": "Gorras y Sombreros" },
            { "id": 60, "name": "Guantes" },
            { "id": 62, "name": "Lentes" },
            { "id": 58, "name": "Mangas" },
            { "id": 59, "name": "Marcas" },
            { "id": 56, "name": "Pelotas" },
            { "id": 179, "name": "Plumas" },
            { "id": 63, "name": "Tees" },
            { "id": 148, "name": "Termos" },
            { "id": 147, "name": "Toallas" },
            { "id": 64, "name": "Zapatera" },
        ]},
        { "id": 149, "name": "Clases", "children": [
            { "id": 165, "name": "Academia de golf" },
            { "id": 164, "name": "Clases de golf" },
            { "id": 162, "name": "Pases" },
            { "id": 163, "name": "Prácticas de golf" },
        ]},
        { "id": 183, "name": "Colindancias" },
        { "id": 153, "name": "Cuotas" },
        { "id": 161, "name": "Green Fees" },
        { "id": 80, "name": "Patrocinios" },
        { "id": 180, "name": "Rentas CG", "children": [
            { "id": 86, "name": "Bastones" },
            { "id": 83, "name": "Carritos" },
        ]},
        { "id": 104, "name": "Ropa", "children": [
            { "id": 66, "name": "Bermudas" },
            { "id": 67, "name": "Calcetines" },
            { "id": 143, "name": "Calzado" },
            { "id": 65, "name": "Faldas / Vestidos" },
            { "id": 41, "name": "Pantalones" },
            { "id": 40, "name": "Playeras" },
            { "id": 141, "name": "Sudaderas" },
        ]},
        { "id": 108, "name": "Torneos de Golf", "children": [
            { "id": 79, "name": "Paraíso Open" },
        ]},
    ]},
    { "id": 35, "name": "CASA CLUB", "children": [
        { "id": 105, "name": "Clases Casa Club" },
        { "id": 150, "name": "Cuidado personal", "children": [
            { "id": 82, "name": "SPA" }
        ]},
        { "id": 81, "name": "Day Pass" },
        { "id": 181, "name": "Eventos", "children": [
            { "id": 78, "name": "Activaciones" },
            { "id": 109, "name": "Eventos Paraíso" },
            { "id": 107, "name": "Eventos Sociales" },
        ]},
        { "id": 182, "name": "Rentas CC", "children": [
            { "id": 160, "name": "Canchas" },
            { "id": 106, "name": "Cavas" },
            { "id": 84, "name": "Lockers" },
        ]},
        { "id": 170, "name": "Servicio de barbería" },
        { "id": 167, "name": "Servicio estética", "children": [
            { "id": 174, "name": "Efectos Premium" },
            { "id": 171, "name": "Manicure Acrílico" },
            { "id": 172, "name": "Manicure con gelish" },
            { "id": 85, "name": "Manicure con rubber y cover" },
            { "id": 173, "name": "Pedicure" },
            { "id": 175, "name": "Servicios adicionales" },
        ]},
    ]},
    { "id": 75, "name": "COLINDANCIAS ***"},
    { "id": 16, "name": "COMIDAS/CENAS", "children": [
        { "id": 129, "name": "Antojitos Mexicanos" },
        { "id": 22, "name": "Aves" },
        { "id": 97, "name": "Botanas" },
        { "id": 159, "name": "Buffet Comida/Cena" },
        { "id": 145, "name": "Burritos/Chapatas/Sandwitches" },
        { "id": 24, "name": "Carnes Rojas" },
        { "id": 26, "name": "Clásicos" },
        { "id": 127, "name": "Enchiladas" },
        { "id": 18, "name": "Ensaladas" },
        { "id": 17, "name": "Entradas" },
        { "id": 146, "name": "Hamburguesas/HotDogs/Pizza" },
        { "id": 23, "name": "Mariscos" },
        { "id": 100, "name": "Menú Infantil" },
        { "id": 21, "name": "Menús Especiales" },
        { "id": 25, "name": "Parrillada" },
        { "id": 20, "name": "Pastas"},
        { "id": 19, "name": "Sopas" },
    ]},
    {"id": 30, "name": "COSTEO"},
    {"id": 1, "name": "DESAYUNOS", "children": [
        {"id": 69, "name": "Buffete Desayuno"},
        {"id": 8, "name": "Cereales y Panes"},
        {"id": 2, "name": "Chilaquiles"},
        {"id": 3, "name": "Clásicos"},
        {"id": 5, "name": "De la Granja", "children": [
            {"id": 128, "name": "Huevos"},
        ]},
        {"id": 4, "name": "Especialidades"},
        {"id": 6, "name": "Fruta"},
    ]},
    {"id": 168, "name": "DESCUENTOS"},
    {"id": 123, "name": "EXTRAS", "children": [
        {"id": 125, "name": "Con costo"},
        {"id": 103, "name": "Modificadores"},
        {"id": 124, "name": "Sin costo"},
    ]},
    {"id": 37, "name": "GUARNICIONES"},
    {"id": 53, "name": "NO DISPONIBLE"},
    {"id": 166, "name": "PERFORMANCE LAB"},
    {"id": 27, "name": "POSTRES", "children": [
        {"id": 158, "name": "Dulces"},
    ]},
    {"id": 48, "name": "RENTAS ***"},
    {"id": 31, "name": "SNACK"},
    {"id": 55, "name": "SUB RECETAS", "children": [
        {"id": 151, "name": "Pastelería"},
        {"id": 152, "name": "Platillos"},
    ]},
    {"id": 111, "name": "SUSHI", "children": [
        {"id": 115, "name": "Bowls"},
        {"id": 156, "name": "Cócteles"},
        {"id": 155, "name": "Ensaladas"},
        {"id": 112, "name": "Entradas"},
        {"id": 121, "name": "Especialidades"},
        {"id": 120, "name": "Extras Sushi"},
        {"id": 126, "name": "Guarniciones Sushi"},
        {"id": 169, "name": "Niguiris"},
        {"id": 119, "name": "Postres"},
        {"id": 154, "name": "Ramen y pastas"},
        {"id": 118, "name": "Rollos empanizados"},
        {"id": 117, "name": "Rollos especiales"},
        {"id": 116, "name": "Rollos tradicionales"},
        {"id": 157, "name": "Sashimi"},
        {"id": 122, "name": "Subrecetas Salsas"},
        {"id": 113, "name": "Tostadas"},
        {"id": 114, "name": "Yakimeshi"},
    ]},
    {"id": 38, "name": "TABACO"},
]


def _flatten(nodes, path=None, out=None):
    if out is None:
        out = []
    path = path or []
    for node in nodes:
        current = path + [(node["id"], node["name"])]
        children = node.get("children") or []
        names = [n for _, n in current]
        record = {
            "id": node["id"],
            "name": node["name"],
            "level": len(current) - 1,
            "is_leaf": len(children) == 0,
            "grupo": names[0] if len(names) >= 1 else "",
            "subgrupo": names[1] if len(names) >= 2 else "",
            "sub_subgrupo": names[2] if len(names) >= 3 else "",
        }
        out.append(record)
        if children:
            _flatten(children, current, out)
    return out


NODES = _flatten(HIERARCHY)
LEAF_NODES = [n for n in NODES if n["is_leaf"]]
