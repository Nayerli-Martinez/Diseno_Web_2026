from flask import Flask, render_template
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_123'


@app.route('/')
def inicio():
    titulo = "Panel Principal"

    resumen = {
        "total_productos": 5,
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

    lista_productos = [
        {"nombre": "Arroz", "categoria": "Granos", "precio": 1.25, "stock": 50},
        {"nombre": "Azúcar", "categoria": "Abarrotes", "precio": 1.10, "stock": 40},
        {"nombre": "Aceite", "categoria": "Víveres", "precio": 3.50, "stock": 25},
        {"nombre": "Leche", "categoria": "Lácteos", "precio": 1.20, "stock": 30},
        {"nombre": "Fideos", "categoria": "Pastas", "precio": 0.85, "stock": 60}
    ]

    return render_template(
        'productos.html',
        productos=lista_productos
    )


@app.route('/formulario-producto', methods=['GET', 'POST'])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "precio": form.precio.data
        }

        print("PRODUCTO REGISTRADO")
        print(producto)

        return render_template(
            'formulario_producto.html',
            form=form,
            mensaje="Producto registrado correctamente"
        )

    if form.is_submitted():
        print("ERRORES:")
        print(form.errors)

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