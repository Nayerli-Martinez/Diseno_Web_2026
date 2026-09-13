CREATE DATABASE IF NOT EXISTS abastos_oferton;

USE abastos_oferton;

CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor)
    REFERENCES proveedores(id_proveedor)
);