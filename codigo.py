import pandas as pd
import re
from datetime import datetime

# ==========================
# CARGA DEL ARCHIVO
# ==========================

print("Cargando archivo...")

df = pd.read_csv("automatas.csv", low_memory=False)

# Eliminar columnas basura
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# ==========================
# VALIDACIONES CON REGEX
# ==========================

patron_usuario = re.compile(r'^[A-Za-z0-9_-]+$')

patron_ip = re.compile(
    r'^(\d{1,3}\.){3}\d{1,3}$'
)

# Patrón MAC flexible que acepta formato estándar y sufijos (ej: :HCDD)
patron_mac = re.compile(
    r'^[0-9A-Fa-f]{2}(-[0-9A-Fa-f]{2}){5}(:[A-Za-z0-9]+)?$'
)

patron_fecha = re.compile(
    r'^\d{4}-\d{2}-\d{2}$'
)

patron_numero = re.compile(
    r'^\d+$'
)

registros_validos = []
registros_invalidos = []

print("Validando registros...")

for _, fila in df.iterrows():

    usuario = str(fila["Usuario"]).strip()
    ip = str(fila["IP_NAS_AP"]).strip()
    fecha = str(fila["Inicio_de_Conexión_Dia"]).strip()
    mac_ap = str(fila["MAC_AP"]).strip()
    mac_cliente = str(fila["MAC_Cliente"]).strip()
    
    # Extraemos los campos numéricos a validar
    input_octects = str(fila["Input_Octects"]).strip()
    output_octects = str(fila["Output_Octects"]).strip()
    session_time = str(fila["Session_Time"]).strip()

    valido = True

    if not patron_usuario.match(usuario):
        valido = False
    if not patron_ip.match(ip):
        valido = False
    if not patron_fecha.match(fecha):
        valido = False
    if not patron_mac.match(mac_ap):
        valido = False
    if not patron_mac.match(mac_cliente):
        valido = False
    if not patron_numero.match(input_octects):
        valido = False
    if not patron_numero.match(output_octects):
        valido = False
    if not patron_numero.match(session_time):
        valido = False

    if valido:
        registros_validos.append(fila)
    else:
        registros_invalidos.append(fila)

df_validos = pd.DataFrame(registros_validos)

print(f"\nRegistros válidos: {len(df_validos)}")
print(f"Registros inválidos: {len(registros_invalidos)}")

# Variable para exportar después
ultimo_resultado = None


# ==========================
# FUNCIONES
# ==========================

def mostrar_macs():

    macs = sorted(df_validos["MAC_AP"].unique())

    print("\n=== LISTA DE MAC AP ===\n")

    for i, mac in enumerate(macs, start=1):
        print(f"{i}. {mac}")

    print(f"\nTotal de AP: {len(macs)}")


def buscar_usuarios():

    global ultimo_resultado

    macs = sorted(df_validos["MAC_AP"].unique())

    print("\n=== MAC AP DISPONIBLES ===\n")

    for i, mac in enumerate(macs, start=1):
        print(f"{i}. {mac}")

    try:
        opcion = int(input("\nSeleccione una MAC AP: "))

        if opcion < 1 or opcion > len(macs):
            print("Opción inválida.")
            return

        mac_seleccionada = macs[opcion - 1]

    except ValueError:
        print("Debe ingresar un número.")
        return

    # Filtramos primero solo por la MAC para ver su historial
    filtrado_ap = df_validos[(df_validos["MAC_AP"] == mac_seleccionada)].copy()
    fechas_reales = pd.to_datetime(filtrado_ap["Inicio_de_Conexión_Dia"])
    min_fecha = fechas_reales.min().strftime('%Y-%m-%d')
    max_fecha = fechas_reales.max().strftime('%Y-%m-%d')

    print(f"\n[DATO CLAVE] Este AP registró actividad desde {min_fecha} hasta {max_fecha}.")
    # ----------------------------------

    fecha_inicio = input("\nFecha inicio (AAAA-MM-DD): ")
    fecha_fin = input("Fecha fin (AAAA-MM-DD): ")

    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        print("Formato de fecha incorrecto.")
        return

    # Aplicamos el filtro de fechas elegido por el usuario
    filtrado_ap["Inicio_de_Conexión_Dia"] = fechas_reales
    filtrado_final = filtrado_ap[
        (filtrado_ap["Inicio_de_Conexión_Dia"] >= fecha_inicio_dt) &
        (filtrado_ap["Inicio_de_Conexión_Dia"] <= fecha_fin_dt)
    ]

    usuarios = sorted(filtrado_final["Usuario"].unique())

    print("\n==============================")
    print("RESULTADO")
    print("==============================")
    print(f"\nMAC AP: {mac_seleccionada}")
    print(f"Periodo: {fecha_inicio} a {fecha_fin}")
    print("\nUsuarios conectados:\n")

    for usuario in usuarios:
        print(usuario)

    print(f"\nCantidad total de usuarios (dispositivos): {len(usuarios)}")

    ultimo_resultado = pd.DataFrame({"Usuario": usuarios})

def exportar_excel():

    global ultimo_resultado

    if ultimo_resultado is None:

        print(
            "\nPrimero debe realizar una búsqueda."
        )
        return

    total = len(ultimo_resultado)

    fila_total = pd.DataFrame(
        {
            "MAC_Cliente": [f"TOTAL: {total}"]
        }
    )

    resultado = pd.concat(
        [ultimo_resultado, fila_total],
        ignore_index=True
    )

    resultado.to_excel(
        "resultado.xlsx",
        index=False
    )

    print(
        "\nArchivo resultado.xlsx generado correctamente."
    )


def mostrar_invalidos():

    print(
        f"\nCantidad de registros descartados: "
        f"{len(registros_invalidos)}"
    )

    if len(registros_invalidos) > 0:

        print(
            "\nPrimeros 10 registros descartados:\n"
        )

        # Para que no explote la consola al imprimir filas completas gigantes de pandas
        for fila in registros_invalidos[:10]:
            print(f"Línea inválida -> MAC AP: {fila.get('MAC_AP', 'N/A')} | Fecha: {fila.get('Inicio_de_Conexión_Dia', 'N/A')}")


# ==========================
# MENÚ PRINCIPAL
# ==========================

# Flujo limpio mediante evaluación de condición
opcion = ""
while opcion != "5":

    print("\n==============================")
    print("ANÁLISIS DE DISPOSITIVOS WIFI")
    print("==============================")

    print("1. Mostrar MAC AP")
    print("2. Buscar usuarios por MAC AP")
    print("3. Exportar resultado a Excel")
    print("4. Mostrar registros descartados")
    print("5. Salir")

    opcion = input("\nSeleccione una opción: ")

    if opcion == "1":
        mostrar_macs()

    elif opcion == "2":
        buscar_usuarios()

    elif opcion == "3":
        exportar_excel()

    elif opcion == "4":
        mostrar_invalidos()

    elif opcion == "5":
        print("\nFin del programa.")

    else:
        print("\nOpción inválida.")