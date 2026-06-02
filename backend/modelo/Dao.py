# modelo/Dao.py
# Basado en el estilo del proyecto CMPG original:
# modelos SQLAlchemy + métodos DAO dentro de cada clase.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'

	user_id = Column(Integer, primary_key=True, autoincrement=True)
	full_name = Column(String(120), nullable=False)
	email = Column(String(120), nullable=False, unique=True)
	password_hash = Column(String(255), nullable=False)
	role = Column(String(50), nullable=False, default='Administrador')
	status = Column(String(20), nullable=False, default='Activo')
	created_at = Column(DateTime, server_default=func.now())

	@property
	def password(self):
		raise AttributeError('La contraseña no se puede leer directamente')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def validarPassword(self, password):
		return check_password_hash(self.password_hash, password)

	def to_dict(self):
		return {
			'user_id': self.user_id,
			'full_name': self.full_name,
			'email': self.email,
			'role': self.role,
			'status': self.status
		}

	def consultaGeneral(self):
		return User.query.order_by(User.user_id).all()

	def consultaIndividual(self, id):
		return User.query.get(id)

	def consultaPorCorreo(self, email):
		return User.query.filter_by(email=email).first()

	def agregar(self):
		db.session.add(self)
		db.session.commit()
		return self


class Category(db.Model):
	__tablename__ = 'categories'

	category_id = Column(Integer, primary_key=True, autoincrement=True)
	category_name = Column(String(100), nullable=False)
	description = Column(String(255))

	products = relationship('Product', back_populates='category', lazy='select')

	def to_dict(self):
		return {
			'category_id': self.category_id,
			'category_name': self.category_name,
			'description': self.description
		}

	def consultaGeneral(self):
		return Category.query.order_by(Category.category_id).all()

	def consultaIndividual(self, id):
		return Category.query.get(id)

	def agregar(self):
		db.session.add(self)
		db.session.commit()
		return self

	def editar(self):
		db.session.merge(self)
		db.session.commit()
		return self

	def eliminar(self, id):
		cat = self.consultaIndividual(id)
		if cat:
			db.session.delete(cat)
			db.session.commit()
			return True
		return False


class Supplier(db.Model):
	__tablename__ = 'suppliers'

	supplier_id = Column(Integer, primary_key=True, autoincrement=True)
	company_name = Column(String(100), nullable=False)
	contact_name = Column(String(100))
	phone = Column(String(50))
	country = Column(String(50))

	products = relationship('Product', back_populates='supplier', lazy='select')

	def to_dict(self):
		return {
			'supplier_id': self.supplier_id,
			'company_name': self.company_name,
			'contact_name': self.contact_name,
			'phone': self.phone,
			'country': self.country
		}

	def consultaGeneral(self):
		return Supplier.query.order_by(Supplier.supplier_id).all()

	def consultaIndividual(self, id):
		return Supplier.query.get(id)


class Product(db.Model):
	__tablename__ = 'products'

	product_id = Column(Integer, primary_key=True, autoincrement=True)
	product_name = Column(String(120), nullable=False)
	supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)
	category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
	quantity_per_unit = Column(String(80))
	unit_price = Column(Float, default=0)
	units_in_stock = Column(Integer, default=0)
	units_on_order = Column(Integer, default=0)
	reorder_level = Column(Integer, default=0)
	discontinued = Column(Boolean, default=False)
	created_at = Column(DateTime, server_default=func.now())

	category = relationship('Category', back_populates='products', lazy='joined')
	supplier = relationship('Supplier', back_populates='products', lazy='joined')
	order_details = relationship('OrderDetail', back_populates='product', lazy='select')

	def to_dict(self):
		return {
			'product_id': self.product_id,
			'product_name': self.product_name,
			'supplier_id': self.supplier_id,
			'supplier_name': self.supplier.company_name if self.supplier else None,
			'category_id': self.category_id,
			'category_name': self.category.category_name if self.category else None,
			'quantity_per_unit': self.quantity_per_unit,
			'unit_price': self.unit_price,
			'units_in_stock': self.units_in_stock,
			'units_on_order': self.units_on_order,
			'reorder_level': self.reorder_level,
			'discontinued': self.discontinued
		}

	def consultaGeneral(self):
		return Product.query.order_by(Product.product_id).all()

	def consultaIndividual(self, id):
		return Product.query.get(id)

	def agregar(self):
		db.session.add(self)
		db.session.commit()
		return self

	def editar(self):
		db.session.merge(self)
		db.session.commit()
		return self

	def eliminar(self, id):
		prod = self.consultaIndividual(id)
		if prod:
			db.session.delete(prod)
			db.session.commit()
			return True
		return False


class Customer(db.Model):
	__tablename__ = 'customers'

	customer_id = Column(String(5), primary_key=True)
	company_name = Column(String(120), nullable=False)
	contact_name = Column(String(100))
	city = Column(String(50))
	country = Column(String(50))

	orders = relationship('Order', back_populates='customer', lazy='select')

	def to_dict(self):
		return {
			'customer_id': self.customer_id,
			'company_name': self.company_name,
			'contact_name': self.contact_name,
			'city': self.city,
			'country': self.country
		}

	def consultaGeneral(self):
		return Customer.query.order_by(Customer.customer_id).all()


class Employee(db.Model):
	__tablename__ = 'employees'

	employee_id = Column(Integer, primary_key=True, autoincrement=True)
	first_name = Column(String(50), nullable=False)
	last_name = Column(String(50), nullable=False)
	title = Column(String(80))

	orders = relationship('Order', back_populates='employee', lazy='select')

	def to_dict(self):
		return {
			'employee_id': self.employee_id,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'full_name': f'{self.first_name} {self.last_name}',
			'title': self.title
		}

	def consultaGeneral(self):
		return Employee.query.order_by(Employee.employee_id).all()


class Order(db.Model):
	__tablename__ = 'orders'

	order_id = Column(Integer, primary_key=True, autoincrement=True)
	customer_id = Column(String(5), ForeignKey('customers.customer_id'), nullable=False)
	employee_id = Column(Integer, ForeignKey('employees.employee_id'), nullable=False)
	order_date = Column(DateTime, server_default=func.now())
	ship_name = Column(String(120))
	ship_address = Column(String(180))
	ship_city = Column(String(80))
	ship_country = Column(String(80))

	customer = relationship('Customer', back_populates='orders', lazy='joined')
	employee = relationship('Employee', back_populates='orders', lazy='joined')
	details = relationship('OrderDetail', back_populates='order', lazy='joined', cascade='all, delete-orphan')

	def to_dict(self, include_details=False):
		data = {
			'order_id': self.order_id,
			'customer_id': self.customer_id,
			'customer_name': self.customer.company_name if self.customer else None,
			'employee_id': self.employee_id,
			'employee_name': self.employee.to_dict()['full_name'] if self.employee else None,
			'order_date': self.order_date.isoformat() if self.order_date else None,
			'ship_name': self.ship_name,
			'ship_address': self.ship_address,
			'ship_city': self.ship_city,
			'ship_country': self.ship_country,
			'total': round(sum((d.unit_price or 0) * (d.quantity or 0) * (1 - (d.discount or 0)) for d in self.details), 2)
		}
		if include_details:
			data['details'] = [d.to_dict() for d in self.details]
		return data

	def consultaGeneral(self):
		return Order.query.order_by(Order.order_id.desc()).all()

	def consultaIndividual(self, id):
		return Order.query.get(id)

	def agregar(self):
		db.session.add(self)
		db.session.commit()
		return self


class OrderDetail(db.Model):
	__tablename__ = 'order_details'

	order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
	unit_price = Column(Float, default=0)
	quantity = Column(Integer, default=1)
	discount = Column(Float, default=0)

	order = relationship('Order', back_populates='details', lazy='joined')
	product = relationship('Product', back_populates='order_details', lazy='joined')

	def to_dict(self):
		return {
			'order_id': self.order_id,
			'product_id': self.product_id,
			'product_name': self.product.product_name if self.product else None,
			'unit_price': self.unit_price,
			'quantity': self.quantity,
			'discount': self.discount,
			'subtotal': round((self.unit_price or 0) * (self.quantity or 0) * (1 - (self.discount or 0)), 2)
		}
