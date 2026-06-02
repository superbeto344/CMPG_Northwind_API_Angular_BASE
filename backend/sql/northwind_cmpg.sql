-- ============================================================
-- Base de datos: northwind_cmpg
-- Proyecto: CMPG Videojuegos + API REST + Angular
-- Descripción:
--   Es una versión estilo Northwind, pero adaptada a una tienda
--   de videojuegos. Conserva la idea de Northwind:
--   categories, suppliers, products, customers, employees,
--   orders y order_details.
-- ============================================================

DROP DATABASE IF EXISTS northwind_cmpg;
CREATE DATABASE northwind_cmpg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE northwind_cmpg;

-- ==============================
-- TABLAS PRINCIPALES
-- ==============================


CREATE TABLE users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	full_name VARCHAR(120) NOT NULL,
	email VARCHAR(120) NOT NULL UNIQUE,
	password_hash VARCHAR(255) NOT NULL,
	role VARCHAR(50) NOT NULL DEFAULT 'Administrador',
	status VARCHAR(20) NOT NULL DEFAULT 'Activo',
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
	category_id INT AUTO_INCREMENT PRIMARY KEY,
	category_name VARCHAR(100) NOT NULL,
	description VARCHAR(255) NOT NULL
);

CREATE TABLE suppliers (
	supplier_id INT AUTO_INCREMENT PRIMARY KEY,
	company_name VARCHAR(100) NOT NULL,
	contact_name VARCHAR(100),
	phone VARCHAR(50),
	country VARCHAR(50)
);

CREATE TABLE products (
	product_id INT AUTO_INCREMENT PRIMARY KEY,
	product_name VARCHAR(120) NOT NULL,
	supplier_id INT NOT NULL,
	category_id INT NOT NULL,
	quantity_per_unit VARCHAR(80),
	unit_price FLOAT DEFAULT 0,
	units_in_stock INT DEFAULT 0,
	units_on_order INT DEFAULT 0,
	reorder_level INT DEFAULT 0,
	discontinued BOOLEAN DEFAULT FALSE,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_products_suppliers FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
	CONSTRAINT fk_products_categories FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE customers (
	customer_id VARCHAR(5) PRIMARY KEY,
	company_name VARCHAR(120) NOT NULL,
	contact_name VARCHAR(100),
	city VARCHAR(50),
	country VARCHAR(50)
);

CREATE TABLE employees (
	employee_id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	title VARCHAR(80)
);

CREATE TABLE orders (
	order_id INT AUTO_INCREMENT PRIMARY KEY,
	customer_id VARCHAR(5) NOT NULL,
	employee_id INT NOT NULL,
	order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	ship_name VARCHAR(120),
	ship_address VARCHAR(180),
	ship_city VARCHAR(80),
	ship_country VARCHAR(80),
	CONSTRAINT fk_orders_customers FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
	CONSTRAINT fk_orders_employees FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE order_details (
	order_id INT NOT NULL,
	product_id INT NOT NULL,
	unit_price FLOAT DEFAULT 0,
	quantity INT DEFAULT 1,
	discount FLOAT DEFAULT 0,
	PRIMARY KEY (order_id, product_id),
	CONSTRAINT fk_details_orders FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
	CONSTRAINT fk_details_products FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Índices para que las búsquedas de Angular/Postman sean más rápidas.
CREATE INDEX idx_products_name ON products(product_name);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_employee ON orders(employee_id);


-- ==============================
-- DATOS: USUARIOS PARA LOGIN
-- Contraseña de ambos: 123456
-- ==============================

INSERT INTO users (full_name, email, password_hash, role, status) VALUES
('Roberto Espinoza', 'admin@cmpg.com', 'pbkdf2:sha256:1000000$cmpg2026$4c681ea166bbf5b5ac079071b055ecfe617c400d6df31fbb2c8dbd87af9635cf', 'Administrador', 'Activo'),
('Empleado CMPG', 'empleado@cmpg.com', 'pbkdf2:sha256:1000000$cmpg2026$4c681ea166bbf5b5ac079071b055ecfe617c400d6df31fbb2c8dbd87af9635cf', 'Vendedor', 'Activo');

-- ==============================
-- DATOS: CATEGORÍAS CMPG
-- ==============================

INSERT INTO categories (category_name, description) VALUES
('Consolas', 'Consolas de videojuegos de sobremesa y portátiles'),
('Videojuegos PC', 'Juegos físicos y digitales para computadora'),
('Videojuegos PlayStation', 'Títulos para consolas PlayStation'),
('Videojuegos Xbox', 'Títulos para consolas Xbox'),
('Videojuegos Nintendo', 'Títulos para consolas Nintendo Switch'),
('Accesorios Gaming', 'Controles, audífonos, teclados, mouse y cargadores'),
('Tarjetas Digitales', 'Gift cards, membresías y saldo digital'),
('Coleccionables', 'Figuras, posters, ediciones especiales y mercancía gamer');

-- ==============================
-- DATOS: PROVEEDORES / DISTRIBUIDORES
-- ==============================

INSERT INTO suppliers (company_name, contact_name, phone, country) VALUES
('GameStage Distribution', 'Laura Méndez', '351-100-2001', 'Mexico'),
('PixelWare Studios', 'Andrés Cortés', '351-100-2002', 'Mexico'),
('Next Level Imports', 'Hiro Tanaka', '+81-03-5555-1101', 'Japan'),
('UltraPlay Mayorista', 'Carlos Ríos', '33-1200-4500', 'Mexico'),
('RetroBit Collectibles', 'Mónica Salazar', '55-4500-8812', 'Mexico'),
('CloudCode Digital', 'Kevin Brooks', '+1-555-720-4455', 'USA'),
('ProGamer Gear', 'Sofía Ortega', '351-777-9900', 'Mexico'),
('RPG World Supply', 'Elena Vargas', '+34-91-555-1200', 'Spain'),
('Arcade Galaxy', 'Roberto Núñez', '351-600-3030', 'Mexico'),
('SpeedRun Storehouse', 'Daniela Torres', '442-555-7788', 'Mexico');

-- ==============================
-- DATOS: PRODUCTOS DE VIDEOJUEGOS
-- product_id inicial: 1 al 32
-- ==============================

INSERT INTO products (product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued) VALUES
('PlayStation 5 Slim 1TB', 1, 1, '1 consola + control DualSense', 9499.00, 8, 3, 2, false),
('Xbox Series X 1TB', 4, 1, '1 consola + control inalámbrico', 8999.00, 6, 2, 2, false),
('Nintendo Switch OLED', 3, 1, '1 consola + dock + Joy-Con', 6499.00, 12, 4, 3, false),
('Steam Deck OLED 512GB', 6, 1, '1 consola portátil', 11999.00, 4, 2, 1, false),
('Halo Infinite PC', 6, 2, 'Código digital para PC', 899.00, 35, 0, 10, false),
('Cyberpunk 2077 Ultimate Edition PC', 6, 2, 'Código digital para PC', 1199.00, 28, 5, 8, false),
('Elden Ring PC', 8, 2, 'Código digital para PC', 1299.00, 22, 3, 6, false),
('Minecraft Java & Bedrock PC', 2, 2, 'Código digital', 599.00, 50, 10, 15, false),
('God of War Ragnarok PS5', 1, 3, 'Caja física PS5', 1299.00, 18, 5, 5, false),
('Spider-Man 2 PS5', 1, 3, 'Caja física PS5', 1399.00, 16, 4, 5, false),
('The Last of Us Part I PS5', 1, 3, 'Caja física PS5', 1199.00, 10, 2, 3, false),
('Gran Turismo 7 PS5', 10, 3, 'Caja física PS5', 1099.00, 13, 0, 4, false),
('Forza Horizon 5 Xbox', 4, 4, 'Caja física Xbox', 999.00, 20, 3, 5, false),
('Gears 5 Xbox', 4, 4, 'Caja física Xbox', 799.00, 15, 0, 5, false),
('Starfield Xbox', 6, 4, 'Código digital Xbox', 1299.00, 17, 6, 5, false),
('Sea of Thieves Xbox', 6, 4, 'Código digital Xbox', 699.00, 24, 5, 8, false),
('The Legend of Zelda Tears of the Kingdom', 3, 5, 'Caja física Nintendo Switch', 1399.00, 14, 4, 4, false),
('Super Mario Bros Wonder', 3, 5, 'Caja física Nintendo Switch', 1299.00, 19, 6, 5, false),
('Mario Kart 8 Deluxe', 3, 5, 'Caja física Nintendo Switch', 1199.00, 21, 2, 6, false),
('Pokemon Legends Arceus', 3, 5, 'Caja física Nintendo Switch', 1199.00, 11, 3, 4, false),
('Control Inalámbrico Xbox Carbon Black', 7, 6, '1 control', 1399.00, 25, 6, 8, false),
('Control DualSense Blanco', 7, 6, '1 control', 1499.00, 23, 4, 8, false),
('Audífonos Gamer RGB 7.1', 7, 6, '1 headset con micrófono', 899.00, 30, 10, 10, false),
('Teclado Mecánico Gamer TKL', 7, 6, '1 teclado switches rojos', 1199.00, 18, 5, 6, false),
('Mouse Gamer 12000 DPI', 7, 6, '1 mouse RGB', 499.00, 40, 12, 12, false),
('Tarjeta Xbox Game Pass 3 Meses', 6, 7, 'Código digital', 749.00, 60, 20, 20, false),
('Tarjeta PlayStation Store 500 MXN', 1, 7, 'Código digital', 500.00, 70, 15, 20, false),
('Tarjeta Nintendo eShop 500 MXN', 3, 7, 'Código digital', 500.00, 65, 12, 20, false),
('Tarjeta Steam Wallet 500 MXN', 6, 7, 'Código digital', 500.00, 80, 20, 20, false),
('Figura Coleccionable Space Warrior', 5, 8, 'Figura 18 cm', 699.00, 12, 0, 3, false),
('Poster Premium RPG Legends', 5, 8, 'Poster 60x90 cm', 249.00, 35, 0, 10, false),
('Edición Coleccionista Arcade Galaxy', 9, 8, 'Caja especial + artbook + soundtrack', 2499.00, 5, 1, 2, false);

-- ==============================
-- DATOS: CLIENTES
-- customer_id usa 5 caracteres al estilo Northwind
-- ==============================

INSERT INTO customers (customer_id, company_name, contact_name, city, country) VALUES
('GMR01', 'Roberto Gamer Store', 'Roberto Espinoza', 'Zamora', 'Mexico'),
('PLY02', 'Pixel Zone Zamora', 'Luis Hernández', 'Zamora', 'Mexico'),
('NVD03', 'Nova Digital', 'Ana Martínez', 'Morelia', 'Mexico'),
('ARC04', 'Arcade House', 'Carlos Jiménez', 'Guadalajara', 'Mexico'),
('RPG05', 'RPG Masters', 'Fernanda López', 'Ciudad de México', 'Mexico'),
('SPD06', 'SpeedRun Shop', 'Jorge Ramírez', 'Querétaro', 'Mexico'),
('RET07', 'RetroBit Fans', 'Diana Salas', 'León', 'Mexico'),
('CLD08', 'Cloud Gaming Center', 'Mario Torres', 'Monterrey', 'Mexico');

-- ==============================
-- DATOS: EMPLEADOS / VENDEDORES
-- ==============================

INSERT INTO employees (first_name, last_name, title) VALUES
('Roberto', 'Espinoza', 'Administrador CMPG'),
('Geddiel', 'Hernández', 'Vendedor de mostrador'),
('Alberto', 'Mora', 'Encargado de inventario'),
('Sofía', 'Ortega', 'Atención a clientes'),
('Daniel', 'Ríos', 'Soporte de ventas online');

-- ==============================
-- DATOS: ÓRDENES
-- ==============================

INSERT INTO orders (customer_id, employee_id, order_date, ship_name, ship_address, ship_city, ship_country) VALUES
('GMR01', 1, '2026-05-01 10:15:00', 'Roberto Gamer Store', 'Av. Juárez 120', 'Zamora', 'Mexico'),
('PLY02', 2, '2026-05-02 12:30:00', 'Pixel Zone Zamora', 'Calle Hidalgo 45', 'Zamora', 'Mexico'),
('NVD03', 4, '2026-05-03 16:20:00', 'Nova Digital', 'Av. Madero 830', 'Morelia', 'Mexico'),
('ARC04', 5, '2026-05-04 09:40:00', 'Arcade House', 'Centro 77', 'Guadalajara', 'Mexico'),
('RPG05', 1, '2026-05-05 18:10:00', 'RPG Masters', 'Insurgentes 300', 'Ciudad de México', 'Mexico'),
('SPD06', 3, '2026-05-06 13:05:00', 'SpeedRun Shop', 'Av. Universidad 25', 'Querétaro', 'Mexico'),
('RET07', 2, '2026-05-07 11:50:00', 'RetroBit Fans', 'Blvd. Campestre 88', 'León', 'Mexico'),
('CLD08', 5, '2026-05-08 15:25:00', 'Cloud Gaming Center', 'Av. Tecnológico 500', 'Monterrey', 'Mexico');

-- ==============================
-- DATOS: DETALLES DE ÓRDENES
-- Relaciona pedidos con productos, igual que Northwind.
-- ==============================

INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount) VALUES
(1, 1, 9499.00, 1, 0),
(1, 22, 1499.00, 1, 0),
(1, 27, 500.00, 2, 0),
(2, 3, 6499.00, 1, 0),
(2, 17, 1399.00, 1, 0.05),
(2, 18, 1299.00, 1, 0),
(3, 5, 899.00, 3, 0),
(3, 8, 599.00, 2, 0),
(3, 29, 500.00, 5, 0),
(4, 2, 8999.00, 1, 0),
(4, 13, 999.00, 2, 0.10),
(4, 21, 1399.00, 2, 0),
(5, 7, 1299.00, 2, 0),
(5, 30, 699.00, 1, 0),
(5, 31, 249.00, 3, 0),
(6, 4, 11999.00, 1, 0),
(6, 6, 1199.00, 1, 0),
(6, 24, 1199.00, 1, 0),
(7, 19, 1199.00, 2, 0),
(7, 20, 1199.00, 1, 0),
(7, 28, 500.00, 3, 0),
(8, 26, 749.00, 4, 0.05),
(8, 23, 899.00, 2, 0),
(8, 32, 2499.00, 1, 0);

-- ==============================
-- CONSULTAS DE VERIFICACIÓN
-- ==============================

SELECT 'Base northwind_cmpg creada correctamente' AS mensaje;
SELECT COUNT(*) AS total_categorias FROM categories;
SELECT COUNT(*) AS total_proveedores FROM suppliers;
SELECT COUNT(*) AS total_productos FROM products;
SELECT COUNT(*) AS total_clientes FROM customers;
SELECT COUNT(*) AS total_empleados FROM employees;
SELECT COUNT(*) AS total_ordenes FROM orders;
SELECT COUNT(*) AS total_detalles FROM order_details;

-- ==============================
-- USUARIO RECOMENDADO PARA LA API
-- Ejecuta este script con root o con un usuario administrador.
-- Después usa estos datos en backend/.env:
-- DB_USER=northwind_user
-- DB_PASSWORD=northwind123
-- DB_NAME=northwind_cmpg
-- ==============================

CREATE USER IF NOT EXISTS 'northwind_user'@'localhost' IDENTIFIED BY 'northwind123';
CREATE USER IF NOT EXISTS 'northwind_user'@'127.0.0.1' IDENTIFIED BY 'northwind123';
GRANT ALL PRIVILEGES ON northwind_cmpg.* TO 'northwind_user'@'localhost';
GRANT ALL PRIVILEGES ON northwind_cmpg.* TO 'northwind_user'@'127.0.0.1';
FLUSH PRIVILEGES;
