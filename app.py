from flask import Flask, render_template, redirect, request, url_for, flash

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import Usuario

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from conexion.conexion import obtener_conexion
from reportlab.pdfgen import canvas
from flask import send_file
import io

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave_secreta_123'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def cargar_usuario(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
        """,
        (id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(
            usuario[0],
            usuario[1]
        )

    return None


@app.route('/')
@login_required
def inicio():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM productos
        """
    )

    total_productos = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM clientes
        """
    )

    total_clientes = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    resumen = {
        "total_productos": total_productos,
        "total_clientes": total_clientes,
        "estado_sistema": "Activo"
    }

    return render_template(
        'index.html',
        titulo="Panel Principal",
        resumen=resumen
    )


@app.route('/dashboard')
@login_required
def dashboard():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM productos
        """
    )

    total_productos = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM clientes
        """
    )

    total_clientes = cursor.fetchone()[0]

    cursor.close()
    conexion.close()

    resumen = {
        "total_productos": total_productos,
        "total_clientes": total_clientes,
        "estado_sistema": "Activo"
    }

    return render_template(
        'dashboard.html',
        resumen=resumen
    )


@app.route('/productos')
@login_required
def productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM productos
        ORDER BY id_producto DESC
        """
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'productos.html',
        productos=productos
    )


@app.route('/formulario-producto', methods=['GET', 'POST'])
@login_required
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

        flash(
            'Producto registrado correctamente.',
            'success'
        )

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form
    )


@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_producto, nombre, precio, stock, id_proveedor
        FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    if not producto:

        cursor.close()
        conexion.close()

        flash(
            'El producto no existe.',
            'danger'
        )

        return redirect(url_for('productos'))

    form = ProductoForm()

    if form.validate_on_submit():

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s,
                precio = %s
            WHERE id_producto = %s
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

        flash(
            'Producto actualizado correctamente.',
            'success'
        )

        return redirect(url_for('productos'))

    if request.method == 'GET':

        form.nombre.data = producto[1]
        form.precio.data = producto[2]

    cursor.close()
    conexion.close()

    return render_template(
        'formulario_producto.html',
        form=form,
        editar=True
    )


@app.route('/eliminar_producto/<int:id>')
@login_required
def eliminar_producto(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_producto
        FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    if not producto:

        cursor.close()
        conexion.close()

        flash(
            'El producto no existe.',
            'danger'
        )

        return redirect(url_for('productos'))

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        'Producto eliminado correctamente.',
        'success'
    )

    return redirect(url_for('productos'))


@app.route('/clientes')
@login_required
def clientes():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM clientes
        ORDER BY id_cliente DESC
        """
    )

    clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'clientes.html',
        clientes=clientes
    )

@app.route('/formulario-cliente', methods=['GET', 'POST'])
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO clientes
            (nombre, email, telefono, direccion)
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                form.direccion.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            'Cliente registrado correctamente.',
            'success'
        )

        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        form=form
    )

@app.route('/proveedores')
@login_required
def proveedores():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT *
        FROM proveedores
        ORDER BY id_proveedor DESC
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'proveedores.html',
        proveedores=proveedores
    )
@app.route('/formulario-proveedor', methods=['GET', 'POST'])
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores
            (nombre, telefono, correo)
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.telefono.data,
                form.correo.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            'Proveedor registrado correctamente.',
            'success'
        )

        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        form=form
    )


@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    factura = None

    if request.method == 'POST':

        id_cliente = request.form['cliente']
        id_producto = request.form['producto']
        cantidad = int(request.form['cantidad'])

        cursor.execute(
            """
            SELECT precio
            FROM productos
            WHERE id_producto = %s
            """,
            (id_producto,)
        )

        producto = cursor.fetchone()

        precio = float(producto[0])
        total = precio * cantidad

        cursor.execute(
            """
            INSERT INTO facturas
            (id_cliente, total)
            VALUES (%s, %s)
            RETURNING id_factura
            """,
            (id_cliente, total)
        )

        id_factura = cursor.fetchone()[0]
        cursor.execute(
                """
                SELECT nombre
                FROM clientes
                WHERE id_cliente = %s
                """,
                (id_cliente,)
            )

        nombre_cliente = cursor.fetchone()[0]

        cursor.execute(
                """
                SELECT nombre
                FROM productos
                WHERE id_producto = %s
                """,
                (id_producto,)
            )

        nombre_producto = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO detalle_factura
            (
                id_factura,
                id_producto,
                cantidad,
                precio,
                subtotal
            )
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                id_factura,
                id_producto,
                cantidad,
                precio,
                total
            )
        )

        conexion.commit()
        factura = {
                "id": id_factura,
                "cliente": nombre_cliente,
                "producto": nombre_producto,
                "cantidad": cantidad,
                "precio": precio,
                "total": total
         }

        flash(
            "Venta registrada correctamente",
            "success"
        )

    cursor.execute(
        "SELECT id_cliente,nombre FROM clientes"
    )

    clientes = cursor.fetchall()

    cursor.execute(
        "SELECT id_producto,nombre FROM productos"
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
    'facturacion.html',
    clientes=clientes,
    productos=productos,
    factura=factura
)


@app.route('/registro', methods=['GET', 'POST'])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        usuario = form.usuario.data.strip()
        password = form.password.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conexion.close()

            flash(
                'El usuario ya existe.',
                'warning'
            )

            return render_template(
                'registro.html',
                form=form
            )

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
            """,
            (
                usuario,
                password_hash
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            'Usuario registrado correctamente.',
            'success'
        )

        return redirect(url_for('login'))

    return render_template(
        'registro.html',
        form=form
    )


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        usuario = form.usuario.data.strip()
        password = form.password.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario,)
        )

        dato = cursor.fetchone()

        cursor.close()
        conexion.close()

        if dato and check_password_hash(
            dato[2],
            password
        ):

            usuario_login = Usuario(
                dato[0],
                dato[1]
            )

            login_user(usuario_login)

            flash(
                'Bienvenido al sistema.',
                'success'
            )

            return redirect(url_for('dashboard'))

        flash(
            'Usuario o contraseña incorrectos.',
            'danger'
        )

    return render_template(
        'login.html',
        form=form
    )


@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'Sesión cerrada correctamente.',
        'success'
    )

    return redirect(url_for('login'))

@app.route('/factura_pdf/<int:id_factura>')
@login_required
def factura_pdf(id_factura):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            f.id_factura,
            c.nombre,
            p.nombre,
            d.cantidad,
            d.precio,
            d.subtotal
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        INNER JOIN detalle_factura d
            ON f.id_factura = d.id_factura
        INNER JOIN productos p
            ON d.id_producto = p.id_producto
        WHERE f.id_factura = %s
        """,
        (id_factura,)
    )

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()

    pdf = io.BytesIO()

    p = canvas.Canvas(pdf)

    # Encabezado
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(300, 800, "ABASTOS EL OFERTON")

    p.line(50, 785, 550, 785)

    p.setFont("Helvetica", 10)
    p.drawString(50, 760, "Direccion: Atuntaqui, Ecuador")
    p.drawString(50, 745, "Telefono: 0999999999")
    p.drawString(50, 730, "Email: abastoseloferton@gmail.com")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 690, "FACTURA DE VENTA")

    # Datos factura
    p.setFont("Helvetica", 12)

    p.drawString(50, 650, f"Factura N°: {factura[0]}")
    p.drawString(50, 625, f"Cliente: {factura[1]}")

    # Tabla encabezado
    p.setFillColorRGB(0.2, 0.6, 0.2)
    p.rect(50, 570, 500, 25, fill=1)

    p.setFillColorRGB(1, 1, 1)
    p.drawString(60, 578, "Producto")
    p.drawString(260, 578, "Cantidad")
    p.drawString(360, 578, "Precio")
    p.drawString(460, 578, "Subtotal")

    # Datos producto
    p.setFillColorRGB(0, 0, 0)

    p.drawString(60, 540, str(factura[2]))
    p.drawString(280, 540, str(factura[3]))
    p.drawString(360, 540, "$" + str(factura[4]))
    p.drawString(460, 540, "$" + str(factura[5]))

    # Total
    p.line(350, 500, 550, 500)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(390, 470, f"TOTAL: ${factura[5]}")

    p.save()

    pdf.seek(0)

    return send_file(
        pdf,
        download_name=f"factura_{id_factura}.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )



if __name__ == '__main__':
    app.run(debug=True)