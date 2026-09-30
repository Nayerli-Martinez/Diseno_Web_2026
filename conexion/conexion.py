import psycopg2

def obtener_conexion():
    conexion = psycopg2.connect(
        host="localhost",
        database="abastos_oferton",
        user="postgres",
        password="admin123"
    )
    return conexion