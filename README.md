# Pipeline de integración y calidad de ventas

**Proyecto demostrativo para la asignatura Fundamentos de Integración y Transformación de Datos.**

## 1. Problema y objetivo
Una empresa almacena clientes y ventas de enero/febrero en archivos CSV. El objetivo es consolidar las ventas, relacionarlas con clientes, detectar errores de calidad y generar salidas auditables **sin eliminar ventas sin correspondencia ni sobrescribir importes reportados**.

## 2. Fuentes
- `data/raw/clientes.csv`: identificador, nombre y ciudad; incluye un identificador repetido.
- `data/raw/ventas_enero.csv`: ventas del primer mes; incluye una venta sin cliente.
- `data/raw/ventas_febrero.csv`: ventas del segundo mes; incluye fecha imposible y total incorrecto.

Todos los datos son **ficticios** y están incluidos en el repositorio para permitir la reproducción.

## 3. Estructura
```text
pipeline_ventas_ejemplo/
├── data/
│   ├── raw/                  # CSV originales
│   └── processed/            # CSV intermedios generados por el pipeline
├── src/
│   ├── __init__.py
│   └── pipeline.py           # Funciones del pipeline
├── outputs/                 # CSV consolidado y reporte JSON generados
├── docs/                    # Documentación complementaria
├── tests/
│   └── test_pipeline.py
├── main.py                   # Punto de entrada
├── requirements.txt
├── .gitignore
└── README.md
```

## 4. Requisitos
- Python 3.10 o superior (recomendado: 3.11).
- Visual Studio Code con extensión Python.
- Conexión a internet para instalar dependencias inicialmente.

## 5. Instalación y ejecución
1. Descomprimir la carpeta y abrir **la carpeta completa** en VS Code: `Archivo > Abrir carpeta`.
2. Abrir `Terminal > Nueva terminal`.
3. Crear entorno virtual:

   Windows (PowerShell):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   macOS / Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   Si PowerShell bloquea la activación, selecciona el intérprete `.venv` en VS Code y ejecuta los comandos usando `\.venv\Scripts\python.exe`.
4. Instalar librerías:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Ejecutar:
   ```bash
   python main.py
   ```
6. Verificar pruebas:
   ```bash
   python -m unittest discover -s tests -v
   ```

Las rutas se calculan a partir de la ubicación de `main.py`, no de la carpeta personal del usuario.

## 6. Etapas del pipeline
1. **Extraer**: lectura de tres CSV y verificación de columnas obligatorias.
2. **Limpiar**: nombres, ciudades sin diferencias de tildes, duplicados de clientes según ID.
3. **Transformar**: `concat` de ventas, fechas parseadas y *Quality Gate* (`total_esperado`, `diferencia`, `total_correcto`).
4. **Integrar**: `merge` izquierdo de ventas con clientes y `validate="many_to_one"`.
5. **Guardar procesados**: clientes limpios y ventas transformadas en `data/processed/`.
6. **Validar**: cantidad de ventas, unicidad de ID y conservación del total reportado.
7. **Guardar salidas**: consolidado CSV y resumen JSON.

## 7. Resultados esperados
- **6 ventas** conservadas.
- **$739.000** de total reportado conservado.
- **1 venta sin cliente**, **1 fecha inválida**, **1 total inconsistente**.
- **1 registro de cliente duplicado por ID** detectado y tratado.
- `data/processed/clientes_limpios.csv`: clientes limpios y deduplicados.
- `data/processed/ventas_transformadas.csv`: ventas concatenadas con fecha parseada y controles monetarios.
- `outputs/ventas_consolidadas.csv`: resultado detallado.
- `outputs/reporte_calidad.json`: indicadores de calidad.

## 8. Decisiones y limitaciones
- Se conserva el primer registro de cada cliente duplicado por ID **solo como regla demostrativa**; en un caso real se debe analizar cuál registro es válido.
- Las ventas sin cliente **no se eliminan**.
- Los totales reportados **no se corrigen automáticamente**; se reporta la discrepancia.
- Las fechas imposibles se marcan como `NaT` y se cuentan.
- La prueba de reproducibilidad consiste en ejecutar los pasos anteriores en un entorno nuevo y comparar los indicadores.

## 9. Seguridad y GitHub
No incluir contraseñas, tokens, credenciales ni datos personales reales. Revisar `git status` antes de `git add .`. `.gitignore` excluye secretos y archivos generados, pero **no elimina archivos sensibles que ya hayan sido registrados en Git**.

Comandos para el primer registro local:
```bash
git init
git branch -M main
git status
git add .
git commit -m "Primera version del pipeline"
```
Después, crear un repositorio vacío en GitHub y ejecutar:
```bash
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```
