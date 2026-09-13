from flask import Flask, render_template, redirect
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'


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

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'productos.html',
        productos=productos
    )


@app.route('/formulario-producto', methods=['GET', 'POST'])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (nombre, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.precio.data,
                10,
                1
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return render_template(
            'formulario_producto.html',
            form=form,
            mensaje="Producto registrado correctamente"
        )

    return render_template(
        'formulario_producto.html',
        form=form
    )


@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET nombre=%s,
                precio=%s
            WHERE id_producto=%s
            """,
            (
                form.nombre.data,
                form.precio.data,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect('/productos')

    return render_template(
        'formulario_producto.html',
        form=form
    )


@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto=%s
        """,
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/productos')


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