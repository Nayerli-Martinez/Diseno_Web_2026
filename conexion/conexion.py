import os
import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        os.environ["DATABASE_URL"]
    )