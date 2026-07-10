# Análisis del IBEX 35 con Python

**Herramienta de consola en Python (pandas + matplotlib) para explorar 24 años de cotizaciones históricas del IBEX 35: máximos y mínimos, variación porcentual, volumen negociado y evolución gráfica entre cualquier par de fechas.**

## Por qué este proyecto

Un histórico de cotizaciones en bruto (6.090 sesiones, de enero de 2000 a diciembre de 2023) no dice nada por sí solo. Este programa lo convierte en respuestas concretas a preguntas de análisis financiero: ¿cuánto llegó a caer el IBEX en una semana concreta? ¿cuánto volumen se negoció en un periodo? ¿cómo evolucionó la cotización entre dos fechas?

Como muestra de esto, el propio dataset contiene un caso de prueba de manual: el **24 de junio de 2016** (día después del referéndum del Brexit) registra una caída del **-12,35% en una sola sesión**, con un volumen **5,5 veces superior** a la media histórica diaria — el programa detecta y cuantifica este tipo de eventos sin necesidad de buscarlos a mano.

## Qué hace

Menú interactivo por consola con 6 opciones:

1. **Cotización máxima y mínima** entre dos fechas.
2. **Variación porcentual** de apertura o cierre entre dos fechas.
3. **Volumen total negociado**, filtrando por un volumen mínimo diario.
4. **Gráfica de evolución** de apertura y cierre, con la banda de máximo-mínimo diario sombreada.
5. **Exportación a CSV** de los datos (fecha, apertura, cierre) del rango seleccionado.
6. Salir.

## Stack técnico

`Python 3` · `pandas` (carga, limpieza y filtrado vectorizado de series temporales) · `matplotlib` (visualización)

## Cómo ejecutarlo

```bash
git clone https://github.com/negana03/analisis-ibex35-python.git
cd analisis-ibex35-python

pip install pandas matplotlib

python analisis_ibex35.py
```

El programa pedirá la ruta al fichero CSV de cotizaciones al arrancar.

## Estructura del repositorio

```
analisis-ibex35-python/
├── analisis_ibex35.py     # Script principal con menú interactivo
├── PrFinal_d.Ibex.csv     # Dataset histórico del IBEX 35 (2000-2023)
├── evolucion_2023.png     # Ejemplo de gráfico generado
└── README.md
```

## Sobre los datos

El dataset contiene cotizaciones diarias del IBEX 35 (fuente: Investing.com) con las columnas fecha, precio de apertura, cierre, máximo, mínimo, volumen negociado y variación porcentual diaria. El programa se encarga de limpiar el formato numérico europeo (separador de miles con punto, decimales con coma) y de normalizar el volumen negociado, expresado indistintamente en millones (M) o miles de millones (B), a una única unidad.

## Notas de diseño

- Todo el filtrado por rango de fechas se apoya en la indexación temporal de pandas (`df.loc[fecha_ini:fecha_fin]`), evitando bucles manuales y validaciones de fecha repetidas en cada consulta.
- Las fechas de inicio y fin se normalizan automáticamente en el orden correcto, sin importar en qué orden las introduzca el usuario.
- La función de exportación y la de gráfico comparten el mismo mecanismo de filtrado que el resto de consultas, evitando lógica duplicada.

## Proyecto desarrollado como parte del Grado en Ciencia de Datos — Universitat de València
