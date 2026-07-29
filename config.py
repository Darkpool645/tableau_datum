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
    { "id": 11, "name": "Sushi"}
]

GROUP_IDS = [
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