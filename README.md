# analisis-ibex35-python
Mini proyecto / práctica universitaria: análisis del IBEX 35 en Python con consultas, métricas de cotización y gráfico de evolución.
Este repositorio contiene un pequeño proyecto desarrollado como práctica del Grado en Ciencia de Datos.  
El objetivo es trabajar con datos históricos del **IBEX 35**, cargarlos desde un fichero y analizarlos mediante diferentes consultas y visualizaciones usando Python.

El programa funciona mediante un menú interactivo que permite elegir qué tipo de análisis realizar sobre las cotizaciones dentro de un rango de fechas.

---

## Funcionalidades del script

A través del menú, el usuario puede:

1. **Obtener la cotización máxima y mínima** entre dos fechas.
2. **Calcular la variación porcentual** entre apertura o cierre en un período.
3. **Calcular el volumen total negociado**, filtrando por un volumen mínimo.
4. **Generar una gráfica** con la evolución de la cotización de apertura.
5. **Exportar a un fichero** los datos entre dos fechas marcadas.
6. **Salir del programa**.

> En resumen: lectura de datos, análisis, cálculos y visualización.  

---

## Requisitos

Para ejecutar el programa necesitas:

- Python 3.x  
- `matplotlib` para las gráficas
