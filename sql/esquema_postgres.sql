-- =========================================
-- BASE DE DATOS ABASTOS OFERTON
-- =========================================

-- TABLA PROVEEDORES
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- TABLA PRODUCTOS
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,

    CONSTRAINT fk_producto_proveedor
    FOREIGN KEY (id_proveedor)
    REFERENCES proveedores(id_proveedor)
);

-- TABLA USUARIOS
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- TABLA CLIENTES
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(150)
);

-- TABLA FACTURAS
CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) DEFAULT 0,

    CONSTRAINT fk_factura_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente)
);

-- TABLA DETALLE FACTURA
CREATE TABLE detalle_factura (
    id_detalle SERIAL PRIMARY KEY,

    id_factura INT NOT NULL,
    id_producto INT NOT NULL,

    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_detalle_factura
    FOREIGN KEY (id_factura)
    REFERENCES facturas(id_factura),

    CONSTRAINT fk_detalle_producto
    FOREIGN KEY (id_producto)
    REFERENCES productos(id_producto)
);

-- =========================================
-- DATOS DE PRUEBA
-- =========================================

INSERT INTO proveedores
(nombre, telefono, correo)
VALUES
(
'Proveedor General',
'0999999999',
'proveedor@gmail.com'
);

INSERT INTO clientes
(nombre, email, telefono, direccion)
VALUES
(
'Carlos Pérez',
'carlos@mail.com',
'0991111111',
'Quito'
),
(
'Ana Gómez',
'ana@mail.com',
'0982222222',
'Quito'
);

INSERT INTO productos
(nombre, precio, stock, id_proveedor)
VALUES
(
'Arroz',
2.50,
100,
1
),
(
'Leche',
1.20,
80,
1
),
(
'Aceite',
3.75,
50,
1
);

INSERT INTO facturas
(id_cliente, total)
VALUES
(
1,
8.70
);

INSERT INTO detalle_factura
(
id_factura,
id_producto,
cantidad,
precio,
subtotal
)
VALUES
(
1,
1,
2,
2.50,
5.00
),
(
1,
2,
1,
1.20,
1.20
),
(
1,
3,
1,
2.50,
2.50
);

-- =========================================
-- CONSULTAS DE PRUEBA
-- =========================================

SELECT * FROM proveedores;
SELECT * FROM productos;
SELECT * FROM clientes;
SELECT * FROM usuarios;
SELECT * FROM facturas;
SELECT * FROM detalle_factura;

-- JOIN CLIENTE + FACTURA
SELECT
f.id_factura,
c.nombre AS cliente,
f.fecha,
f.total
FROM facturas f
INNER JOIN clientes c
ON f.id_cliente = c.id_cliente;

-- JOIN COMPLETO
SELECT
f.id_factura,
c.nombre AS cliente,
p.nombre AS producto,
d.cantidad,
d.precio,
d.subtotal
FROM detalle_factura d
INNER JOIN facturas f
ON d.id_factura = f.id_factura
INNER JOIN clientes c
ON f.id_cliente = c.id_cliente
INNER JOIN productos p
ON d.id_producto = p.id_producto;

CREATE TABLE facturas (
    id_factura SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_factura_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);

CREATE TABLE detalle_factura (
    id_detalle SERIAL PRIMARY KEY,
    id_factura INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    CONSTRAINT fk_detalle_factura
        FOREIGN KEY (id_factura)
        REFERENCES facturas(id_factura),
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
);
