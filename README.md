# Análisis de Dispositivos WiFi

Trabajo práctico realizado en Python para analizar registros de conexión de dispositivos WiFi a partir de un archivo CSV.  
El programa permite validar datos, filtrar usuarios por MAC AP y rango de fechas, exportar resultados a Excel y revisar registros descartados.

## Integrantes

- Abigail Palacios
- Gabriela Vacca
- Dana Tinnerello
- Ignacio Quercetti
- Santiago Stacchiola

## Descripción

El sistema lee el archivo `automatas.csv` y realiza validaciones sobre distintos campos mediante expresiones regulares:

- Usuario
- IP_NAS_AP
- Inicio_de_Conexión_Dia
- MAC_AP

A partir de eso, separa los registros válidos de los inválidos y ofrece un menú interactivo con las siguientes opciones:

1. Mostrar las MAC AP disponibles.
2. Buscar usuarios conectados por MAC AP y rango de fechas.
3. Exportar el resultado de la búsqueda a Excel.
4. Mostrar registros descartados.
5. Salir.

## Requisitos

- Python 3.x
- Pandas
- Openpyxl

## Ejecución

'''bash

./manager.sh

'''