from flask import Flask, render_template
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'

DB_PATH = os.path.join('data', 'eloferton.db')


def crear_bd():
    os.makedirs('data', exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


crear_bd()


@app.route('/')
def inicio():

    titulo = "Panel Principal"

    resumen = {
        "total_productos": 0,
        "total_clientes": 3,
        "estado_sistema": "Activo"
    }

    return render_template(
        'index.html',
        titulo=titulo,
        resumen=resumen
    )


@app.route('/productos')
def productos():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conn.close()

    return render_template(
        'productos.html',
        productos=productos
    )


@app.route('/formulario-producto', methods=['GET', 'POST'])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO productos(nombre, precio)
            VALUES (?, ?)
            """,
            (
                form.nombre.data,
                form.precio.data
            )
        )

        conn.commit()
        conn.close()

        return render_template(
            'formulario_producto.html',
            form=form,
            mensaje="Producto registrado correctamente"
        )

    return render_template(
        'formulario_producto.html',
        form=form
    )


@app.route('/clientes')
def clientes():

    lista_clientes = [
        {
            "nombre": "Carlos Pérez",
            "email": "carlos@mail.com",
            "tipo": "Frecuente"
        },
        {
            "nombre": "Ana Gómez",
            "email": "ana@mail.com",
            "tipo": "Regular"
        }
    ]

    return render_template(
        'clientes.html',
        clientes=lista_clientes
    )


@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')


@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')


if __name__ == '__main__':
    app.run(debug=True)