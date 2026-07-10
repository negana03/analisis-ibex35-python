"""
Análisis del IBEX 35
=====================

Contamos con un archivo CSV con las cotizaciones históricas del IBEX 35
(formato exportado de Investing.com), con las columnas:

    "Fecha", "Último", "Apertura", "Máximo", "Mínimo", "Vol.", "% var."

Este programa carga esos datos en un DataFrame de pandas y ofrece un menú
interactivo por consola con 6 opciones para consultar máximos/mínimos,
variación porcentual, volumen negociado, evolución gráfica y exportación
de datos entre dos fechas dadas.

Autora: Galera Navarro, Nerea
"""

from __future__ import annotations

import sys
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Carga y limpieza de datos
# ---------------------------------------------------------------------------

def _limpiar_numero(serie: pd.Series) -> pd.Series:
    """Convierte una columna de texto tipo '10.146,00' a float 10146.00."""
    return (
        serie.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )


def _limpiar_volumen(serie: pd.Series) -> pd.Series:
    """Convierte el volumen a float, en millones.

    '210,70M' -> 210.70   (ya está en millones)
    '1,08B'   -> 1080.0   (miles de millones -> millones)
    """
    serie = serie.astype(str)
    es_billones = serie.str.contains("B")
    numero = (
        serie.str.replace("M", "", regex=False)
        .str.replace("B", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    numero[es_billones] = numero[es_billones] * 1000
    return numero


def _limpiar_porcentaje(serie: pd.Series) -> pd.Series:
    """Convierte '-1,09%' a float -1.09."""
    return (
        serie.astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )


def cargar_datos(ruta: str) -> pd.DataFrame:
    """Carga el CSV de cotizaciones y devuelve un DataFrame limpio.

    El DataFrame resultante está indexado por fecha, ordenado de forma
    ascendente (de la más antigua a la más reciente), con las columnas
    numéricas ya convertidas a float.

    Parameters
    ----------
    ruta : str
        Ruta al fichero CSV de cotizaciones.

    Returns
    -------
    pd.DataFrame
        Datos de cotización indexados por fecha.

    Raises
    ------
    FileNotFoundError
        Si el fichero no existe o no se puede leer.
    """
    df = pd.read_csv(ruta, encoding="utf-8-sig")

    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d.%m.%Y")
    for columna in ["Último", "Apertura", "Máximo", "Mínimo"]:
        df[columna] = _limpiar_numero(df[columna])

    df["Volumen_M"] = _limpiar_volumen(df["Vol."])
    df["Variacion_%"] = _limpiar_porcentaje(df["% var."])

    df = (
        df.drop(columns=["Vol.", "% var."])
        .sort_values("Fecha")
        .set_index("Fecha")
    )

    return df


# ---------------------------------------------------------------------------
# Entrada de fechas
# ---------------------------------------------------------------------------

def pedir_fecha(df: pd.DataFrame, mensaje: str = "fecha") -> pd.Timestamp:
    """Pide al usuario día, mes y año, y valida que estén dentro del rango
    de datos disponible.

    Parameters
    ----------
    df : pd.DataFrame
        Datos de cotización indexados por fecha.
    mensaje : str
        Etiqueta descriptiva para el prompt (p. ej. "fecha inicial").

    Returns
    -------
    pd.Timestamp
        Fecha introducida, validada dentro del rango del dataset.
    """
    fecha_min, fecha_max = df.index.min(), df.index.max()

    while True:
        print(f"\nIntroduzca la {mensaje} "
              f"(entre {fecha_min:%d/%m/%Y} y {fecha_max:%d/%m/%Y}):")
        try:
            dia = int(input("  Día: "))
            mes = int(input("  Mes: "))
            anio = int(input("  Año: "))
            fecha = pd.Timestamp(year=anio, month=mes, day=dia)
        except (ValueError, TypeError):
            print("  Fecha no válida, inténtelo de nuevo.")
            continue

        if fecha_min <= fecha <= fecha_max:
            return fecha
        print("  Fecha fuera del rango disponible en los datos.")


def pedir_rango_fechas(df: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Pide una fecha inicial y una final, devolviéndolas siempre en orden
    (inicial <= final), independientemente del orden en que se introduzcan.
    """
    f1 = pedir_fecha(df, "fecha inicial")
    f2 = pedir_fecha(df, "fecha final")
    return (f1, f2) if f1 <= f2 else (f2, f1)


# ---------------------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------------------

def cotizacion_max_min(
    df: pd.DataFrame, fecha_ini: pd.Timestamp, fecha_fin: pd.Timestamp
) -> tuple[float, float]:
    """Cotización máxima y mínima registradas entre dos fechas (inclusive)."""
    rango = df.loc[fecha_ini:fecha_fin]
    return rango["Máximo"].max(), rango["Mínimo"].min()


def variacion_porcentual(
    df: pd.DataFrame,
    fecha_ini: pd.Timestamp,
    fecha_fin: pd.Timestamp,
    columna: str,
) -> float:
    """Variación porcentual de una columna (Apertura o Último) entre dos
    fechas.

    Parameters
    ----------
    columna : str
        'Apertura' o 'Último'.
    """
    rango = df.loc[fecha_ini:fecha_fin, columna]
    if len(rango) < 2:
        print("No hay suficientes datos entre las fechas dadas.")
        return 0.0

    valor_inicio, valor_fin = rango.iloc[0], rango.iloc[-1]
    return round((valor_fin - valor_inicio) / valor_inicio * 100, 4)


def volumen_total(
    df: pd.DataFrame,
    fecha_ini: pd.Timestamp,
    fecha_fin: pd.Timestamp,
    vol_min: float,
) -> float:
    """Volumen total negociado entre dos fechas, contando solo los días en
    los que el volumen supera un mínimo dado (en millones)."""
    rango = df.loc[fecha_ini:fecha_fin, "Volumen_M"]
    return rango[rango > vol_min].sum()


# ---------------------------------------------------------------------------
# Gráfico y exportación
# ---------------------------------------------------------------------------

def graficar_evolucion(
    df: pd.DataFrame,
    fecha_ini: pd.Timestamp,
    fecha_fin: pd.Timestamp,
    guardar_como: str | None = None,
) -> None:
    """Dibuja la evolución de la cotización de apertura y cierre entre dos
    fechas, con una banda sombreada entre el máximo y el mínimo diario.
    """
    rango = df.loc[fecha_ini:fecha_fin]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.fill_between(
        rango.index, rango["Mínimo"], rango["Máximo"],
        color="steelblue", alpha=0.15, label="Rango máximo-mínimo diario",
    )
    ax.plot(rango.index, rango["Apertura"], color="steelblue",
            linewidth=1.3, label="Apertura")
    ax.plot(rango.index, rango["Último"], color="darkorange",
            linewidth=1.3, label="Cierre")

    ax.set_title(
        f"Evolución del IBEX 35 ({fecha_ini:%d/%m/%Y} - {fecha_fin:%d/%m/%Y})"
    )
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Puntos")
    ax.legend(loc="best")
    fig.autofmt_xdate()
    fig.tight_layout()

    if guardar_como:
        fig.savefig(guardar_como, dpi=150)
        print(f"Gráfico guardado en '{guardar_como}'.")

    plt.show()


def exportar_datos(
    df: pd.DataFrame, fecha_ini: pd.Timestamp, fecha_fin: pd.Timestamp
) -> str:
    """Exporta fecha, apertura y cierre entre dos fechas a un CSV.

    Returns
    -------
    str
        Nombre del fichero generado.
    """
    rango = df.loc[fecha_ini:fecha_fin, ["Apertura", "Último"]].rename(
        columns={"Último": "Cierre"}
    )

    nombre_fichero = (
        f"ibex35_{fecha_ini:%Y%m%d}_a_{fecha_fin:%Y%m%d}.csv"
    )
    rango.to_csv(nombre_fichero, encoding="utf-8")
    return nombre_fichero


# ---------------------------------------------------------------------------
# Menú
# ---------------------------------------------------------------------------

OPCIONES_MENU = """
--------------------- Menú IBEX 35 ---------------------
1) Cotización máxima y mínima entre dos fechas.
2) Variación porcentual (apertura o cierre) entre dos fechas.
3) Volumen total negociado entre dos fechas (con volumen mínimo).
4) Gráfica de evolución de la cotización entre dos fechas.
5) Exportar datos (fecha, apertura, cierre) entre dos fechas a CSV.
6) Salir.
"""


def menu_opciones() -> int:
    """Muestra el menú y devuelve la opción elegida por el usuario."""
    print(OPCIONES_MENU)
    while True:
        try:
            return int(input("Por favor, elija una opción: "))
        except ValueError:
            print("Por favor, introduzca un número.")


def main() -> None:
    print(__doc__)
    ruta = input("Introduzca la ruta del fichero CSV: ").strip()

    try:
        df = cargar_datos(ruta)
    except (FileNotFoundError, OSError):
        print("Error al abrir el fichero. Programa finalizado.")
        sys.exit(1)

    print(f"Datos cargados: {len(df)} sesiones, "
          f"de {df.index.min():%d/%m/%Y} a {df.index.max():%d/%m/%Y}.")

    opcion = menu_opciones()
    while opcion != 6:

        if opcion == 1:
            f1, f2 = pedir_rango_fechas(df)
            cot_max, cot_min = cotizacion_max_min(df, f1, f2)
            print(f"\nMáximo: {cot_max:.2f}   Mínimo: {cot_min:.2f}")

        elif opcion == 2:
            f1, f2 = pedir_rango_fechas(df)
            col = input("Apertura (A) o Cierre (C): ").strip().upper()
            columna = "Apertura" if col == "A" else "Último"
            variacion = variacion_porcentual(df, f1, f2, columna)
            print(f"\nVariación porcentual: {variacion}%")

        elif opcion == 3:
            f1, f2 = pedir_rango_fechas(df)
            vol_min = float(input("Volumen mínimo a considerar (millones): "))
            total = volumen_total(df, f1, f2, vol_min)
            print(f"\nVolumen total negociado: {total:.2f} M")

        elif opcion == 4:
            f1, f2 = pedir_rango_fechas(df)
            graficar_evolucion(df, f1, f2)

        elif opcion == 5:
            f1, f2 = pedir_rango_fechas(df)
            nombre = exportar_datos(df, f1, f2)
            print(f"\nDatos exportados a '{nombre}'.")

        else:
            print("Opción no válida.")

        opcion = menu_opciones()

    print("Cerrando el programa...")


if __name__ == "__main__":
    main()
