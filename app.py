from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    # Variable simple y diccionario
    titulo = "Panel Principal"
    resumen = {"total_productos": 4, "total_clientes": 3, "estado_sistema": "Activo"}
    return render_template('index.html', titulo=titulo, resumen=resumen)

@app.route('/productos')
def productos():
    # Lista de diccionarios para iterar con {% for %} y evaluar con {% if %}
    lista_productos = [
        {"nombre": "laptop dell", "categoria": "tecnología", "precio": 750.00, "stock": 8},
        {"nombre": "mouse óptico", "categoria": "accesorios", "precio": 15.50, "stock": 0},
        {"nombre": "teclado mecánico", "categoria": "accesorios", "precio": 45.00, "stock": 12},
        {"nombre": "monitor 24 pulg", "categoria": "pantallas", "precio": 180.00, "stock": 3}
    ]
    return render_template('productos.html', productos=lista_productos)

@app.route('/clientes')
def clientes():
    lista_clientes = [
        {"nombre": "Carlos Pérez", "email": "carlos@mail.com", "tipo": "VIP"},
        {"nombre": "Ana Gómez", "email": "ana@mail.com", "tipo": "Regular"}
    ]
    return render_template('clientes.html', clientes=lista_clientes)

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)