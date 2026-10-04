from flask import Flask, render_template, redirect, request, session, url_for, flash

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
from flask import Flask, render_template, request, redirect, url_for, flash, session

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

    if request.method == 'POST':

        print("========== POST PRODUCTO ==========")
        print("Nombre:", request.form.get('nombre'))
        print("Precio:", request.form.get('precio'))
        print("Stock:", request.form.get('stock'))

        if not form.validate():
            print("ERRORES:", form.errors)

            return render_template(
                'formulario_producto.html',
                form=form
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO productos
                (nombre, precio, stock, id_proveedor)
                VALUES (%s, %s, %s, %s)
            """, (
                form.nombre.data,
                form.precio.data,
                form.stock.data,
                1
            ))

            conexion.commit()

            print("******** PRODUCTO GUARDADO ********")

            flash('Producto registrado correctamente.', 'success')

            return redirect(url_for('productos'))

        except Exception as e:
            conexion.rollback()

            print("******** ERROR SQL ********")
            print(e)

            flash(f'Error SQL: {e}', 'danger')

            return render_template(
                'formulario_producto.html',
                form=form
            )

        finally:
            cursor.close()
            conexion.close()

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
                precio = %s,
                stock = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.precio.data,
                form.stock.data,
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
        form.stock.data = producto[3]

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
@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, email, telefono, direccion
        FROM clientes
        WHERE id_cliente = %s
    """, (id,))

    cliente = cursor.fetchone()

    if not cliente:
        cursor.close()
        conexion.close()
        flash('El cliente no existe.', 'danger')
        return redirect(url_for('clientes'))

    form = ClienteForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                email = %s,
                telefono = %s,
                direccion = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            form.direccion.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))

    if request.method == 'GET':
        form.nombre.data = cliente[1]
        form.correo.data = cliente[2]
        form.telefono.data = cliente[3]
        form.direccion.data = cliente[4]

    cursor.close()
    conexion.close()

    return render_template(
        'formulario_cliente.html',
        form=form,
        editar=True
    )


@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash('Cliente eliminado correctamente.', 'success')

    return redirect(url_for('clientes'))

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
@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre, telefono, correo
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    proveedor = cursor.fetchone()

    if not proveedor:
        cursor.close()
        conexion.close()

        flash('El proveedor no existe.', 'danger')
        return redirect(url_for('proveedores'))

    form = ProveedorForm()

    if form.validate_on_submit():

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash('Proveedor actualizado correctamente.', 'success')

        return redirect(url_for('proveedores'))

    if request.method == 'GET':
        form.nombre.data = proveedor[1]
        form.telefono.data = proveedor[2]
        form.correo.data = proveedor[3]

    cursor.close()
    conexion.close()

    return render_template(
        'formulario_proveedor.html',
        form=form,
        editar=True
    )


@app.route('/eliminar_proveedor/<int:id>')
@login_required
def eliminar_proveedor(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash('Proveedor eliminado correctamente.', 'success')

    return redirect(url_for('proveedores'))


@app.route('/facturacion')
@login_required
def facturacion():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_venta, fecha, total
        FROM ventas
        ORDER BY id_venta DESC
    """)

    ventas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'facturacion.html',
        ventas=ventas
    )
@app.route('/detalle-factura/<int:id_venta>')
@login_required
def detalle_factura(id_venta):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            v.id_venta,
            v.fecha,
            v.total,
            p.nombre,
            d.cantidad,
            d.precio,
            d.subtotal
        FROM ventas v
        JOIN detalle_venta d
            ON d.id_venta = v.id_venta
        JOIN productos p
            ON p.id_producto = d.id_producto
        WHERE v.id_venta = %s
        ORDER BY d.id_detalle
    """, (id_venta,))

    detalles = cursor.fetchall()

    cursor.close()
    conexion.close()

    if not detalles:
        flash('La venta no existe.', 'danger')
        return redirect(url_for('facturacion'))

    return render_template(
        'detalle_factura.html',
        detalles=detalles,
        id_venta=id_venta
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

@app.route('/factura_pdf/<int:id_venta>')
@login_required
def factura_pdf(id_venta):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            v.id_venta,
            v.fecha,
            v.total,
            p.nombre,
            d.cantidad,
            d.precio,
            d.subtotal
        FROM ventas v
        INNER JOIN detalle_venta d
            ON v.id_venta = d.id_venta
        INNER JOIN productos p
            ON d.id_producto = p.id_producto
        WHERE v.id_venta = %s
        ORDER BY d.id_detalle
    """, (id_venta,))

    detalles = cursor.fetchall()

    cursor.close()
    conexion.close()

    if not detalles:
        flash('La venta no existe.', 'danger')
        return redirect(url_for('facturacion'))

    pdf = io.BytesIO()

    p = canvas.Canvas(pdf)

    # ==============================
    # ENCABEZADO
    # ==============================

    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(300, 800, "ABASTOS EL OFERTON")

    p.line(50, 785, 550, 785)

    p.setFont("Helvetica", 10)
    p.drawString(50, 760, "Direccion: Atuntaqui, Ecuador")
    p.drawString(50, 745, "Telefono: 0999999999")
    p.drawString(50, 730, "Email: abastoseloferton@gmail.com")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 690, "FACTURA DE VENTA")

    # ==============================
    # DATOS DE LA VENTA
    # ==============================

    p.setFont("Helvetica", 12)

    p.drawString(
        50,
        650,
        f"Factura N°: {detalles[0][0]}"
    )

    p.drawString(
        50,
        625,
        f"Fecha: {detalles[0][1]}"
    )

    # ==============================
    # ENCABEZADO TABLA
    # ==============================

    p.setFillColorRGB(0.2, 0.6, 0.2)
    p.rect(50, 570, 500, 25, fill=1)

    p.setFillColorRGB(1, 1, 1)

    p.drawString(60, 578, "Producto")
    p.drawString(260, 578, "Cantidad")
    p.drawString(360, 578, "Precio")
    p.drawString(460, 578, "Subtotal")

    # ==============================
    # PRODUCTOS
    # ==============================

    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica", 10)

    y = 540

    for detalle in detalles:

        nombre_producto = detalle[3]
        cantidad = detalle[4]
        precio = detalle[5]
        subtotal = detalle[6]

        p.drawString(
            60,
            y,
            str(nombre_producto)
        )

        p.drawString(
            280,
            y,
            str(cantidad)
        )

        p.drawString(
            360,
            y,
            f"${float(precio):.2f}"
        )

        p.drawString(
            460,
            y,
            f"${float(subtotal):.2f}"
        )

        y -= 25

    # ==============================
    # TOTAL
    # ==============================

    total = detalles[0][2]

    p.line(350, y - 10, 550, y - 10)

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        390,
        y - 40,
        f"TOTAL: ${float(total):.2f}"
    )

    p.setFont("Helvetica", 10)

    p.drawCentredString(
        300,
        y - 80,
        "Gracias por su compra"
    )

    p.save()

    pdf.seek(0)

    return send_file(
        pdf,
        download_name=f"factura_{id_venta}.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )

@app.route('/nueva-venta')
@login_required
def nueva_venta():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_producto, nombre, precio, stock
        FROM productos
        WHERE stock > 0
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    carrito = session.get('carrito', [])

    return render_template(
        'nueva_venta.html',
        productos=productos,
        carrito=carrito
    )

@app.route('/agregar-al-carrito', methods=['POST'])
@login_required
def agregar_al_carrito():

    id_producto = int(request.form['id_producto'])
    cantidad = int(request.form['cantidad'])

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_producto, nombre, precio, stock
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if producto is None:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('nueva_venta'))

    if cantidad <= 0:
        flash('La cantidad debe ser mayor a 0.', 'danger')
        return redirect(url_for('nueva_venta'))

    if cantidad > producto[3]:
        flash('No hay suficiente stock.', 'danger')
        return redirect(url_for('nueva_venta'))

    carrito = session.get('carrito', [])

    encontrado = False

    for item in carrito:
        if item['id_producto'] == id_producto:
            nueva_cantidad = item['cantidad'] + cantidad

            if nueva_cantidad > producto[3]:
                flash('No hay suficiente stock.', 'danger')
                return redirect(url_for('nueva_venta'))

            item['cantidad'] = nueva_cantidad
            item['subtotal'] = float(producto[2]) * nueva_cantidad
            encontrado = True
            break

    if not encontrado:

        carrito.append({
            'id_producto': producto[0],
            'nombre': producto[1],
            'precio': float(producto[2]),
            'cantidad': cantidad,
            'subtotal': float(producto[2]) * cantidad
        })

    session['carrito'] = carrito
    session.modified = True

    return redirect(url_for('nueva_venta'))
@app.route('/finalizar-venta')
@login_required
def finalizar_venta():

    carrito = session.get('carrito', [])

    if not carrito:
        flash('No hay productos en la venta.', 'warning')
        return redirect(url_for('nueva_venta'))

    total = sum(item['subtotal'] for item in carrito)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            INSERT INTO ventas (total)
            VALUES (%s)
            RETURNING id_venta
        """, (total,))

        id_venta = cursor.fetchone()[0]

        for item in carrito:

            cursor.execute("""
                INSERT INTO detalle_venta
                (id_venta, id_producto, cantidad, precio, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                id_venta,
                item['id_producto'],
                item['cantidad'],
                item['precio'],
                item['subtotal']
            ))

            cursor.execute("""
                UPDATE productos
                SET stock = stock - %s
                WHERE id_producto = %s
            """, (
                item['cantidad'],
                item['id_producto']
            ))

        conexion.commit()

        session.pop('carrito', None)

        flash(
            'Venta registrada correctamente.',
            'success'
        )

        return redirect(url_for('productos'))

    except Exception as e:

        conexion.rollback()

        print("ERROR EN VENTA:", e)

        flash(
            f'ERROR: {e}',
            'danger'
        )

        return redirect(url_for('nueva_venta'))

    finally:

        cursor.close()
        conexion.close()


if __name__ == '__main__':
    app.run(debug=True)