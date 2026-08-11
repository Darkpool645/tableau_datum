# Extracción de Datos para Tableros DATUM

Script en Python que automatiza la extracción de reportes de venta desde el sistema DATUM (vía scraping con sesión autenticada) y los exporta en formato JSONL para alimentar tableros de análisis.

## ¿Qué hace?

1. Inicia sesión en DATUM usando las credenciales configuradas.
2. Revisa `ventas.jsonl`: si ya existe, retoma la extracción al día siguiente de la última fecha guardada; si no, arranca desde el 1 de enero de 2025. En ambos casos llega hasta el día anterior a la ejecución.
3. Divide ese rango en tramos mensuales y, dentro de cada tramo, en combinaciones de **todas las áreas × día** (un día a la vez, porque el reporte de DATUM agrega todo el rango pedido en una sola fila por área/producto/tipo y no trae fecha por fila).
4. Para cada combinación, construye la URL del reporte de ventas y descarga la tabla de resultados.
5. Limpia y normaliza cada fila (convierte campos numéricos, descarta filas de totales/encabezados).
6. Al terminar cada mes, agrega sus registros a `ventas.jsonl` de inmediato (así el progreso queda a salvo si la ejecución se interrumpe).
7. Reintenta automáticamente las combinaciones que fallaron, con espera exponencial (hasta 3 rondas).
8. Si quedan combinaciones sin recuperar tras los reintentos, las guarda en `fallidas.json`.

## Requerimientos

* Python 3.14+
* Git

## Instalación

```bash
git clone <url-del-repositorio>
cd reportes_venta_datum
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Copia el archivo de ejemplo y completa tus credenciales de DATUM:

```bash
cp .env.example .env
```

Variables requeridas en `.env`:

| Variable          | Descripción                                |
|-------------------|---------------------------------------------|
| `DATUM_USERNAME`  | Usuario de acceso al sistema DATUM          |
| `DATUM_PASSWORD`  | Contraseña de acceso al sistema DATUM       |
| `DATUM_BASE`      | URL base del sistema DATUM                  |

Las áreas a extraer se configuran en [config.py](config.py) (`AREAS`).

## Uso

```bash
python main.py
```

Al finalizar, el script muestra en consola la cobertura obtenida (combinaciones completadas vs. totales) y el número de registros extraídos.

## Salidas

* **`ventas.jsonl`** — un registro JSON por línea con los campos: `area`, `producto`, `tipo`, `cantidad`, `precio`, `impuesto`, `total`, `costo`, `margen`, `utilidad`, `date`.
* **`fallidas.json`** — combinaciones de área/fecha que no se pudieron recuperar tras los reintentos (solo se genera si hubo fallos).

`fallidas.json` se limpia al inicio de cada ejecución. `ventas.jsonl` **no** se borra: cada corrida retoma la extracción a partir de la última fecha ya guardada en el archivo.

## Estructura del proyecto

```
main.py       # Punto de entrada: orquesta el flujo de extracción y escritura
scraper.py    # Login, generación de combinaciones y scraping del reporte
utils.py      # Limpieza y normalización de filas extraídas
config.py     # Credenciales, áreas, grupos de productos y parámetros del reporte
```
