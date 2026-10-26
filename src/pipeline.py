"""Funciones reutilizables de extracción, limpieza, integración y validación."""
from pathlib import Path
import unicodedata
import pandas as pd

CLIENT_COLUMNS = {"id_cliente", "nombre", "ciudad"}
SALE_COLUMNS = {"id_venta", "id_cliente", "fecha", "cantidad", "precio_unitario", "total_reportado"}


def leer_csv(ruta: Path, columnas: set[str]) -> pd.DataFrame:
    if not ruta.is_file():
        raise FileNotFoundError(f"Falta archivo de entrada: {ruta}")
    df = pd.read_csv(ruta, encoding="utf-8")
    faltantes = columnas - set(df.columns)
    if faltantes:
        raise ValueError(f"{ruta.name}: faltan columnas {sorted(faltantes)}")
    return df


def extraer(carpeta: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    clientes = leer_csv(carpeta / "clientes.csv", CLIENT_COLUMNS)
    enero = leer_csv(carpeta / "ventas_enero.csv", SALE_COLUMNS)
    febrero = leer_csv(carpeta / "ventas_febrero.csv", SALE_COLUMNS)
    return clientes, enero, febrero


def normalizar_ciudad(valor: object) -> object:
    if pd.isna(valor):
        return valor
    texto = unicodedata.normalize("NFKD", str(valor).strip())
    return "".join(c for c in texto if not unicodedata.combining(c)).upper()


def limpiar_clientes(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    datos = df.copy()
    datos["nombre"] = datos["nombre"].astype("string").str.strip().str.title()
    datos["ciudad"] = datos["ciudad"].map(normalizar_ciudad)
    # La política de este ejemplo conserva la primera aparición de cada cliente.
    # En datos reales, conflictos entre filas requieren una regla de negocio.
    repetidos = int(datos.duplicated(subset=["id_cliente"]).sum())
    datos = datos.drop_duplicates(subset=["id_cliente"], keep="first")
    return datos, repetidos


def transformar_ventas(enero: pd.DataFrame, febrero: pd.DataFrame) -> pd.DataFrame:
    ventas = pd.concat([enero.copy(), febrero.copy()], ignore_index=True)
    ventas["fecha_parseada"] = pd.to_datetime(ventas["fecha"], format="%d/%m/%Y", errors="coerce")
    ventas["total_esperado"] = ventas["cantidad"] * ventas["precio_unitario"]
    ventas["diferencia"] = ventas["total_reportado"] - ventas["total_esperado"]
    ventas["total_correcto"] = ventas["diferencia"].eq(0)
    return ventas


def integrar(ventas: pd.DataFrame, clientes: pd.DataFrame) -> pd.DataFrame:
    return ventas.merge(clientes, on="id_cliente", how="left", validate="many_to_one", indicator=True)


def validar(resultado: pd.DataFrame, ventas: pd.DataFrame) -> dict:
    if len(resultado) != len(ventas):
        raise ValueError("La integración alteró el número de ventas")
    if not resultado["id_venta"].is_unique:
        raise ValueError("Hay identificadores de venta duplicados")
    if resultado["total_reportado"].sum() != ventas["total_reportado"].sum():
        raise ValueError("La integración alteró el total reportado")
    return {
        "ventas_entrada": len(ventas),
        "ventas_salida": len(resultado),
        "total_reportado": int(resultado["total_reportado"].sum()),
        "ventas_sin_cliente": int(resultado["_merge"].eq("left_only").sum()),
        "fechas_invalidas": int(resultado["fecha_parseada"].isna().sum()),
        "totales_inconsistentes": int((~resultado["total_correcto"]).sum()),
    }


def guardar(resultado: pd.DataFrame, reporte: dict, carpeta: Path) -> None:
    import json
    carpeta.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(carpeta / "ventas_consolidadas.csv", index=False, encoding="utf-8-sig")
    (carpeta / "reporte_calidad.json").write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")


def guardar_procesados(clientes: pd.DataFrame, ventas: pd.DataFrame, carpeta: Path) -> None:
    """Conserva tablas limpias antes del merge para facilitar auditoría."""
    carpeta.mkdir(parents=True, exist_ok=True)
    clientes.to_csv(carpeta / "clientes_limpios.csv", index=False, encoding="utf-8-sig")
    ventas.to_csv(carpeta / "ventas_transformadas.csv", index=False, encoding="utf-8-sig")
