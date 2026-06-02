# CMPG Northwind API + Angular - Guía de uso

Proyecto basado en CMPG, adaptado a **API REST con Flask + MySQL** y **frontend Angular**.

Incluye lo que pide la práctica:

- Inicio de sesión.
- Mínimo 5 tablas: `users`, `categories`, `suppliers`, `products`, `customers`, `employees`, `orders`, `order_details`.
- Navegación funcional con navbar.
- Formularios: login, productos, categorías y órdenes.
- Consumo de API REST desde Angular usando `HttpClient`.
- Colección de Postman.
- `.gitignore` para subir el frontend/proyecto a GitHub sin `node_modules`, `venv` ni `.env`.

---

## 1. Programas necesarios

Instala solo esto:

1. Python 3.10 o superior.
2. MySQL Server y MySQL Workbench.
3. Node.js LTS.
4. Angular CLI:

```powershell
npm install -g @angular/cli
```

5. Postman.
6. Git o GitHub Desktop, solo si vas a subirlo a GitHub.

No necesitas XAMPP, WAMP, PHP ni SQL Server.

---

## 2. Crear la base de datos

Abre MySQL Workbench y ejecuta completo este archivo:

```text
backend/sql/northwind_cmpg.sql
```

Ese script crea la base:

```sql
northwind_cmpg
```

También inserta datos de videojuegos, clientes, empleados, órdenes y usuarios.

Usuarios de prueba para login:

```text
Correo: admin@cmpg.com
Contraseña: 123456
```

```text
Correo: empleado@cmpg.com
Contraseña: 123456
```

---

## 3. Configurar backend

Entra a la carpeta backend:

```powershell
cd backend
```

Crea el entorno virtual:

```powershell
python -m venv venv
```

Actívalo:

```powershell
venv\Scripts\activate
```

Instala dependencias:

```powershell
pip install -r requirements.txt
```

El archivo `requirements.txt` ya incluye:

```text
cryptography==45.0.7
```

Esto evita el error de MySQL:

```text
cryptography package is required for sha256_password or caching_sha2_password
```

---

## 4. Crear archivo .env

Copia:

```text
backend/.env.example
```

Y renómbralo a:

```text
backend/.env
```

Ejemplo:

```env
DB_USER=root
DB_PASSWORD=TU_PASSWORD_DE_MYSQL
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=northwind_cmpg
```

Si usaste un usuario diferente, cámbialo ahí.

---

## 5. Correr backend Flask

Desde `backend` ejecuta:

```powershell
python app.py
```

Debe abrirse en:

```text
http://127.0.0.1:5000
```

Prueba en navegador:

```text
http://127.0.0.1:5000/api/health
```

---

## 6. Probar API en Postman

Importa el archivo:

```text
postman_collection.json
```

La variable debe ser:

```text
base_url = http://127.0.0.1:5000/api
```

Pruebas principales:

```text
POST /auth/login
GET /users
GET /categories
POST /categories
GET /products
POST /products
PUT /products/:id
DELETE /products/:id
GET /customers
GET /employees
GET /orders
POST /orders
```

Nota: no borres productos originales que ya tienen órdenes. Para probar DELETE, primero crea un producto nuevo y borra ese producto.

---

## 7. Correr Angular

Abre otra terminal. No cierres Flask.

Entra a frontend:

```powershell
cd frontend
```

Instala dependencias:

```powershell
npm install
```

Corre Angular:

```powershell
npm start
```

Se abrirá:

```text
http://localhost:4200
```

Entra con:

```text
Correo: admin@cmpg.com
Contraseña: 123456
```

---

## 8. Qué revisar en Angular

Después de iniciar sesión tendrás navbar con:

- Productos.
- Categorías.
- Órdenes.
- Clientes.
- Empleados.
- Usuarios.
- Cerrar sesión.

Los módulos consumen la API REST de Flask. Si Flask está apagado, Angular cargará pero no mostrará datos.

---

## 9. Orden correcto para ejecutar

Siempre usa dos terminales:

Terminal 1:

```powershell
cd backend
venv\Scripts\activate
python app.py
```

Terminal 2:

```powershell
cd frontend
npm start
```

---

## 10. Subir frontend a GitHub

Si el profe solo pidió el repositorio del frontend, puedes subir la carpeta `frontend` o todo el proyecto.

Antes de subir, revisa que `.gitignore` tenga:

```gitignore
venv/
.env
node_modules/
dist/
.angular/
__pycache__/
```

Comandos desde la raíz del proyecto:

```powershell
git init
git add .
git commit -m "Proyecto CMPG Northwind API REST Angular con login"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

Si Git no funciona, instala Git for Windows o usa GitHub Desktop.

---

## 11. Cómo explicarlo al profesor

Este proyecto usa Flask como backend API REST conectado a MySQL con SQLAlchemy. La base es una adaptación de Northwind a una tienda de videojuegos CMPG. Angular funciona como frontend y consume los endpoints REST con HttpClient. El sistema tiene login, navbar, formularios CRUD, consulta de varias tablas y pruebas en Postman.
