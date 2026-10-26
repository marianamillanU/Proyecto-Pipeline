"""Punto de entrada: ejecutar con `python main.py` desde cualquier carpeta."""
from pathlib import Path
from src.pipeline import extraer, limpiar_clientes, transformar_ventas, integrar, validar, guardar, guardar_procesados

BASE = Path(__file__).resolve().parent


def main() -> None:
    print("1/6 Extrayendo archivos...")
    clientes, enero, febrero = extraer(BASE / "data" / "raw")
    print("2/6 Limpiando y transformando...")
    clientes, duplicados = limpiar_clientes(clientes)
    ventas = transformar_ventas(enero, febrero)
    print("3/6 Guardando datos intermedios en data/processed...")
    guardar_procesados(clientes, ventas, BASE / "data" / "processed")
    print("4/6 Integrando clientes y ventas...")
    resultado = integrar(ventas, clientes)
    print("5/6 Validando integridad...")
    reporte = validar(resultado, ventas)
    reporte["clientes_duplicados_por_id"] = duplicados
    print("6/6 Guardando salidas...")
    guardar(resultado, reporte, BASE / "outputs")
    for clave, valor in reporte.items():
        print(f"  {clave}: {valor}")
    print("Listo: revisa data/processed/ y outputs/")


if __name__ == "__main__":
    main()
