# Extracción de Datos para Tableros DATUM

Script en Python que automatiza la extracción de reportes de venta desde el sistema DATUM (vía scraping con sesión autenticada) y los exporta en formato JSONL para alimentar tableros de análisis.

## ¿Qué hace?

1. Inicia sesión en DATUM usando las credenciales configuradas.
2. Genera todas las combinaciones de **área × día** desde el 1 de enero de 2025 hasta la fecha actual.
3. Para cada combinación, construye la URL del reporte de ventas y descarga la tabla de resultados.
4. Limpia y normaliza cada fila (convierte campos numéricos, descarta filas de totales/encabezados).
5. Reintenta automáticamente las combinaciones que fallaron, con espera exponencial (hasta 3 rondas).
6. Escribe los registros extraídos en `ventas.jsonl` y, si quedan combinaciones sin recuperar, las guarda en `fallidas.json`.

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

Las áreas y grupos de productos a extraer se configuran en [config.py](config.py) (`AREAS` y `TYPE_IDS`).

## Uso

```bash
python main.py
```

Al finalizar, el script muestra en consola la cobertura obtenida (combinaciones completadas vs. totales) y el número de registros extraídos.

## Salidas

* **`ventas.jsonl`** — un registro JSON por línea con los campos: `area`, `producto`, `tipo`, `cantidad`, `precio`, `impuesto`, `total`, `costo`, `margen`, `utilidad`, `date`.
* **`fallidas.json`** — combinaciones de área/fecha que no se pudieron recuperar tras los reintentos (solo se genera si hubo fallos).

Ambos archivos se limpian automáticamente al inicio de cada ejecución.

## Estructura del proyecto

```
main.py       # Punto de entrada: orquesta el flujo de extracción y escritura
scraper.py    # Login, generación de combinaciones y scraping del reporte
utils.py      # Limpieza y normalización de filas extraídas
config.py     # Credenciales, áreas, grupos de productos y parámetros del reporte
```
