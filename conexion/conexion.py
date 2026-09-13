import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2026",
        database="abastos_oferton"
    )
    return conexion