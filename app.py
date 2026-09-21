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


@app.route('/facturacion')
@login_required
def facturacion():

    return render_template(
        'facturacion.html'
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


if __name__ == '__main__':
    app.run(debug=True)