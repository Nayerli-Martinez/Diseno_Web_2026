from conexion.conexion import obtener_conexion

try:
    conexion = obtener_conexion()
    print("CONEXIÓN EXITOSA A POSTGRESQL")
    conexion.close()
except Exception as e:
    print("ERROR DE CONEXIÓN:")
    print(e)
