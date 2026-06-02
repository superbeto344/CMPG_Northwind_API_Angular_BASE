# Backend Flask - CMPG Northwind API

## Ejecutar

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Base de datos

Ejecuta en MySQL Workbench:

```text
backend/sql/northwind_cmpg.sql
```

## Login de prueba

```text
Correo: admin@cmpg.com
Contraseña: 123456
```

## Endpoints principales

```text
POST /api/auth/login
GET  /api/users
GET  /api/categories
POST /api/categories
GET  /api/products
POST /api/products
PUT  /api/products/:id
DELETE /api/products/:id
GET  /api/customers
GET  /api/employees
GET  /api/orders
POST /api/orders
```
