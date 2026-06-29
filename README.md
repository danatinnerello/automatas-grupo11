# Análisis de Dispositivos WiFi

Trabajo práctico realizado en Python para analizar registros de conexión de dispositivos WiFi a partir de un archivo CSV.  
El programa permite validar datos mediante expresiones regulares, filtrar usuarios por MAC AP y rango de fechas, exportar resultados a Excel y gestionar los registros descartados.

## Integrantes

- Abigail Palacios
- Gabriela Vaca
- Dana Tinnerello
- Ignacio Quercetti
- Santiago Stacchiola

## Descripción

El sistema lee el archivo `automatas.csv` y realiza validaciones sobre distintos campos utilizando Expresiones Regulares (Regex):

- Usuario
- IP_NAS_AP
- Inicio_de_Conexión_Dia
- MAC_AP

A partir de este análisis, separa los registros válidos de los inválidos y ofrece un menú interactivo con las siguientes opciones:

1. Mostrar las MAC AP disponibles.
2. Buscar usuarios conectados por MAC AP y rango de fechas.
3. Exportar el resultado de la búsqueda a Excel (Genera `resultado.xlsx`).
4. Mostrar registros descartados.
5. Exportar registros descartados a Excel (Genera `descartados.xlsx`).
6. Salir.

## Requisitos e Instalación

- Python 3.x
- Pandas
- Openpyxl

Puedes instalar las dependencias necesarias ejecutando el siguiente comando:
```bash
pip install pandas openpyxl