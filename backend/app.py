# app.py
# API REST Northwind para Angular
# Adaptado tomando como base el proyecto CMPG original:
# - Flask
# - SQLAlchemy
# - carpeta modelo/Dao.py
# - rutas CRUD parecidas a las de productos/categorías del proyecto anterior
# Ejecutar: python app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from config import Config
from modelo.Dao import (
	db, User, Category, Supplier, Product, Customer,
	Employee, Order, OrderDetail
)


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app)

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({'error': 'Recurso no encontrado'}), 404

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({'error': 'Solicitud incorrecta'}), 400

	@app.get('/api/health')
	def health():
		return jsonify({
			'status': 'ok',
			'message': 'API REST Northwind funcionando',
			'base': 'Proyecto CMPG adaptado a API REST + Angular'
		})


	# ==============================
	# AUTENTICACIÓN / LOGIN
	# ==============================
	@app.post('/api/auth/login')
	def login():
		data = request.get_json() or {}
		email = (data.get('email') or '').strip().lower()
		password = data.get('password') or ''

		if not email or not password:
			return jsonify({'error': 'Correo y contraseña son obligatorios'}), 400

		user = User().consultaPorCorreo(email)

		if not user or not user.validarPassword(password) or user.status != 'Activo':
			return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401

		return jsonify({
			'message': 'Inicio de sesión correcto',
			'token': f'cmpg-token-{user.user_id}',
			'user': user.to_dict()
		})

	@app.post('/api/auth/register')
	def register():
		data = request.get_json() or {}

		if not data.get('full_name') or not data.get('email') or not data.get('password'):
			return jsonify({'error': 'Nombre, correo y contraseña son obligatorios'}), 400

		email = data.get('email').strip().lower()

		if User().consultaPorCorreo(email):
			return jsonify({'error': 'El correo ya está registrado'}), 409

		user = User(
			full_name=data.get('full_name'),
			email=email,
			role=data.get('role') or 'Administrador',
			status='Activo'
		)
		user.password = data.get('password')
		user.agregar()

		return jsonify(user.to_dict()), 201

	@app.get('/api/users')
	def get_users():
		users = User().consultaGeneral()
		return jsonify([u.to_dict() for u in users])

	# ==============================
	# CATEGORIAS
	# ==============================
	@app.get('/api/categories')
	def get_categories():
		categories = Category().consultaGeneral()
		return jsonify([c.to_dict() for c in categories])

	@app.get('/api/categories/<int:category_id>')
	def get_category(category_id):
		category = Category().consultaIndividual(category_id)
		if not category:
			return jsonify({'error': 'Categoría no encontrada'}), 404
		return jsonify(category.to_dict())

	@app.post('/api/categories')
	def create_category():
		data = request.get_json() or {}
		if not data.get('category_name'):
			return jsonify({'error': 'El nombre de la categoría es obligatorio'}), 400

		category = Category(
			category_name=data.get('category_name'),
			description=data.get('description')
		)
		category.agregar()
		return jsonify(category.to_dict()), 201

	@app.put('/api/categories/<int:category_id>')
	def update_category(category_id):
		category = Category().consultaIndividual(category_id)
		if not category:
			return jsonify({'error': 'Categoría no encontrada'}), 404

		data = request.get_json() or {}
		category.category_name = data.get('category_name', category.category_name)
		category.description = data.get('description', category.description)
		category.editar()
		return jsonify(category.to_dict())

	@app.delete('/api/categories/<int:category_id>')
	def delete_category(category_id):
		category = Category().consultaIndividual(category_id)
		if not category:
			return jsonify({'error': 'Categoría no encontrada'}), 404

		related = Product.query.filter_by(category_id=category_id).count()
		if related > 0:
			return jsonify({'error': 'No se puede eliminar: la categoría tiene productos relacionados'}), 409

		db.session.delete(category)
		db.session.commit()
		return jsonify({'message': 'Categoría eliminada correctamente'})

	# ==============================
	# PROVEEDORES
	# ==============================
	@app.get('/api/suppliers')
	def get_suppliers():
		suppliers = Supplier().consultaGeneral()
		return jsonify([s.to_dict() for s in suppliers])

	# ==============================
	# PRODUCTOS
	# ==============================
	@app.get('/api/products')
	def get_products():
		search = request.args.get('search', '').strip()
		category_id = request.args.get('category_id', type=int)

		query = Product.query

		if search:
			query = query.filter(Product.product_name.like(f'%{search}%'))

		if category_id:
			query = query.filter(Product.category_id == category_id)

		products = query.order_by(Product.product_id).all()
		return jsonify([p.to_dict() for p in products])

	@app.get('/api/products/<int:product_id>')
	def get_product(product_id):
		product = Product().consultaIndividual(product_id)
		if not product:
			return jsonify({'error': 'Producto no encontrado'}), 404
		return jsonify(product.to_dict())

	@app.post('/api/products')
	def create_product():
		data = request.get_json() or {}

		required = ['product_name', 'supplier_id', 'category_id']
		for field in required:
			if not data.get(field):
				return jsonify({'error': f'El campo {field} es obligatorio'}), 400

		product = Product(
			product_name=data.get('product_name'),
			supplier_id=data.get('supplier_id'),
			category_id=data.get('category_id'),
			quantity_per_unit=data.get('quantity_per_unit'),
			unit_price=float(data.get('unit_price') or 0),
			units_in_stock=int(data.get('units_in_stock') or 0),
			units_on_order=int(data.get('units_on_order') or 0),
			reorder_level=int(data.get('reorder_level') or 0),
			discontinued=bool(data.get('discontinued', False))
		)

		try:
			product.agregar()
			return jsonify(product.to_dict()), 201
		except IntegrityError:
			db.session.rollback()
			return jsonify({'error': 'Proveedor o categoría no válidos'}), 400

	@app.put('/api/products/<int:product_id>')
	def update_product(product_id):
		product = Product().consultaIndividual(product_id)
		if not product:
			return jsonify({'error': 'Producto no encontrado'}), 404

		data = request.get_json() or {}

		product.product_name = data.get('product_name', product.product_name)
		product.supplier_id = data.get('supplier_id', product.supplier_id)
		product.category_id = data.get('category_id', product.category_id)
		product.quantity_per_unit = data.get('quantity_per_unit', product.quantity_per_unit)
		product.unit_price = float(data.get('unit_price', product.unit_price or 0))
		product.units_in_stock = int(data.get('units_in_stock', product.units_in_stock or 0))
		product.units_on_order = int(data.get('units_on_order', product.units_on_order or 0))
		product.reorder_level = int(data.get('reorder_level', product.reorder_level or 0))
		product.discontinued = bool(data.get('discontinued', product.discontinued))

		try:
			product.editar()
			return jsonify(product.to_dict())
		except IntegrityError:
			db.session.rollback()
			return jsonify({'error': 'Proveedor o categoría no válidos'}), 400

	@app.delete('/api/products/<int:product_id>')
	def delete_product(product_id):
		product = Product().consultaIndividual(product_id)
		if not product:
			return jsonify({'error': 'Producto no encontrado'}), 404

		related = OrderDetail.query.filter_by(product_id=product_id).count()
		if related > 0:
			return jsonify({'error': 'No se puede eliminar: el producto está relacionado con órdenes'}), 409

		db.session.delete(product)
		db.session.commit()
		return jsonify({'message': 'Producto eliminado correctamente'})

	# ==============================
	# CLIENTES Y EMPLEADOS
	# ==============================
	@app.get('/api/customers')
	def get_customers():
		customers = Customer().consultaGeneral()
		return jsonify([c.to_dict() for c in customers])

	@app.get('/api/employees')
	def get_employees():
		employees = Employee().consultaGeneral()
		return jsonify([e.to_dict() for e in employees])

	# ==============================
	# ORDENES
	# ==============================
	@app.get('/api/orders')
	def get_orders():
		orders = Order().consultaGeneral()
		return jsonify([o.to_dict() for o in orders])

	@app.get('/api/orders/<int:order_id>')
	def get_order(order_id):
		order = Order().consultaIndividual(order_id)
		if not order:
			return jsonify({'error': 'Orden no encontrada'}), 404
		return jsonify(order.to_dict(include_details=True))

	@app.post('/api/orders')
	def create_order():
		data = request.get_json() or {}
		details = data.get('details') or []

		if not data.get('customer_id') or not data.get('employee_id'):
			return jsonify({'error': 'customer_id y employee_id son obligatorios'}), 400

		if len(details) == 0:
			return jsonify({'error': 'La orden debe tener al menos un detalle'}), 400

		order = Order(
			customer_id=data.get('customer_id'),
			employee_id=data.get('employee_id'),
			ship_name=data.get('ship_name'),
			ship_address=data.get('ship_address'),
			ship_city=data.get('ship_city'),
			ship_country=data.get('ship_country')
		)

		try:
			db.session.add(order)
			db.session.flush()

			for item in details:
				product_id = item.get('product_id')
				product = Product.query.get(product_id)

				if not product:
					db.session.rollback()
					return jsonify({'error': f'Producto {product_id} no encontrado'}), 404

				quantity = int(item.get('quantity') or 1)
				unit_price = float(item.get('unit_price') or product.unit_price or 0)
				discount = float(item.get('discount') or 0)

				detail = OrderDetail(
					order_id=order.order_id,
					product_id=product_id,
					unit_price=unit_price,
					quantity=quantity,
					discount=discount
				)
				db.session.add(detail)

				if product.units_in_stock is not None:
					product.units_in_stock = max(0, product.units_in_stock - quantity)

			db.session.commit()
			return jsonify(order.to_dict(include_details=True)), 201

		except IntegrityError:
			db.session.rollback()
			return jsonify({'error': 'Cliente, empleado o producto no válido'}), 400

	return app


app = create_app()

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)
