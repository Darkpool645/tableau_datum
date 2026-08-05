import os
from dotenv import load_dotenv

load_dotenv()

DATUM_USER = os.getenv('DATUM_USERNAME')
DATUM_PASSWORD = os.getenv('DATUM_PASSWORD')
DATUM_BASE_URL = os.getenv('DATUM_BASE')

AREAS = [
    { "id": 1, "name": "Restaurante Vista al Lago" },
    { "id": 4, "name": "Carrito 1" },
    { "id": 5, "name": "Carrito 2" },
    { "id": 7, "name": "Hoyo 10" },
    { "id": 3, "name": "Mulligan" },
    { "id": 15, "name": "Servicio a Domicilio" },
    { "id": 19, "name": "Callos de cortes" },
    { "id": 11, "name": "Sushi"},
    { "id": 22, "name": "Estética" },
    { "id": 20, "name": "Performance Lab" },
    { "id": 2, "name": "Proshop" }
]

TYPE_IDS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
    21, 22, 23, 24, 25, 26, 27,
    30, 31, 32, 35, 37, 38,
    40, 41, 48,
    53, 55, 56, 57, 58, 59,
    60, 62, 63, 64, 65, 66, 67, 68, 69,
    75, 78, 79, 
    80, 89,
    90, 91, 92, 93, 94, 95, 96, 97,
    100, 102, 103, 104, 105, 106, 107, 108, 109,
    111, 112, 113, 114, 115, 116, 117, 118, 119,
    120, 121, 122, 123, 123, 125, 126, 127, 128, 129,
    130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
    140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
    150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
    160, 161, 162, 163, 164, 165, 166, 167, 168, 169,
    170
]

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
        { "id": 181, "name": "Eventos", "cildren": [
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
            "path_ids": [i for i, _ in current],
        }
        out.append(record)
        if children:
            _flatten(children, current, out)
    return out

NODES = _flatten(HIERARCHY)
LEAF_NODES = [n for n in NODES if n["is_leaf"]]

GROUP_IDS = [n["id"] for n in NODES if n["level"] == 0]
SUBGROUP_IDS = [n["id"] for n in NODES if n["level"] == 1]
SUB_SUBGROUP_IDS = [n["id"] for n in NODES if n["level"] == 2]

PATH_BY_ID = {
    n["id"]: { "grupo": n["grupo"], "subgrupo": n["subgrupo"], "sub_subgrupo": n["sub_subgrupo"]}
    for n in NODES
}

# Estrategia de consulta
#   "leaves"        -> consulta solo nodos hoja (menos peticiones; asume que los productos viven en el nivel más profundo disponible).
#   "all_nodes"     -> consulta todos los nodos y, al duplicar, se queda con la etiqueta más profunda (más completo, más peticiones).
QUERY_STRATEGY = "leaves"

def query_nodes():
    if QUERY_STRATEGY == "all_nodes":
        return NODES
    return LEAF_NODES

STATIC_PARAMS = (
    "frBusco=1&frBoton=Buscar&frTipo1=1&frTipo2=1&frTipo3=1&frTipo4=1&frTipo5=1&"
    "frStatus2=1&frStatus3=1&frStatus4=1&frStatus5=1&frCorte=&frTipoProducto1=1&frTipoProducto2=1&"
    "frTipoProducto3=1&frTipoProducto4=1&frTipoProducto5=1&frTipoProducto6=1&frTipoProducto7=1&"
    "frTipoProducto8=1&frTipoProducto9=1&frTipoProducto11=1&frTipoProducto12=1&frTipoProducto13=1&"
    "frTipoProducto14=1&frTipoProducto15=1&frTipoProducto16=1&frTipoProducto17=1&frTipoProducto18=1&"
    "frTipoProducto20=1&frTipoProducto21=1&frTipoProducto22=1&frTipoProducto23=1&frTipoProducto24=1&"
    "frTipoProducto25=1&frTipoProducto26=1&frTipoProducto27=1&frTipoProducto28=1&frTipoProducto29=1&"
    "frTipoProducto30=1&frTipoProducto31=1&frTipoProducto32=1&frTipoProducto33=1&frTipoProducto34=1&"
    "frTipoProducto35=1&frTipoProducto36=1&frTipoProducto37=1&frTipoProducto38=1&frTipoProducto39=1&"
    "frTipoProducto40=1&frTipoProducto41=1&frTipoProducto42=1&frTipoProducto43=1&frTipoProducto44=1&"
    "frTipoProducto45=1&frTipoProducto46=1&frTipoProducto47=1&frTipoProducto48=1&frTipoProducto49=1&"
    "frTipoProducto50=1&frMesero=&frProductoVendido=1&frProductoCancelado=1&frFeliz=&frDia0=1&"
    "frDia1=1&frDia2=1&frDia3=1&frDia4=1&frDia5=1&frDia6=1&frHora0=1&frHora1=1&frHora2=1&frHora3=1&"
    "frHora4=1&frHora5=1&frHora6=1&frHora7=1&frHora8=1&frHora9=1&frHora10=1&frHora11=1&frHora12=1&"
    "frHora13=1&frHora14=1&frHora15=1&frHora16=1&frHora17=1&frHora18=1&frHora19=1&frHora20=1&"
    "frHora21=1&frHora22=1&frHora23=1&frProducto=&frPrecio_inicio=&frPrecio_final=&frPorcion_inicio=&"
    "frPorcion_final=&frMinutos1_inicio=&frMinutos1_final=&frMinutos2_inicio=&frMinutos2_final=&"
    "frMinutos3_inicio=&frMinutos3_final=&frMinutos4_inicio=&frMinutos4_final=&frReporte=detallado"
)

FIELDS = [
    "area", "producto", "tipo", "cantidad", "precio",
    "impuesto", "total", "costo", "margen", "utilidad"
]

GROUP_FIELDS = ["grupo", "subgrupo", "sub_subgrupo"]

NUM_COLS = len(FIELDS)
NUMERIC = { "cantidad", "precio", "impuesto", "total", "costo", "margen", "utilidad" }

AREA_MAP = {
    "Callos" : "Callos de cortes",
    "Carrito 1" : "Carrito 1",
    "Carrito 2" : "Carrito 2",
    "Hoyo 10" : "Hoyo 10",
    "Sushi" : "Sushi",
    "Mulligan" : "Mulligan",
    "Vista" : "Restaurante Vista del Lago"
}

PROTECTED_AREAS = {
    "Servicio a Domicilio"
}