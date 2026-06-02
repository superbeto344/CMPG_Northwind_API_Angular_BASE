import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Customer, Employee, Product, Order } from '../../models/models';

@Component({
	selector: 'app-ordenes',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './ordenes.component.html'
})
export class OrdenesComponent implements OnInit {
	orders: Order[] = [];
	customers: Customer[] = [];
	employees: Employee[] = [];
	products: Product[] = [];

	error = '';
	success = '';

	form = {
		customer_id: 'ALFKI',
		employee_id: 1,
		ship_name: 'Cliente de prueba',
		ship_address: 'Calle prueba 123',
		ship_city: 'Zamora',
		ship_country: 'Mexico',
		product_id: 1,
		quantity: 1
	};

	constructor(private api: ApiService) {}

	ngOnInit(): void {
		this.loadCatalogs();
		this.loadOrders();
	}

	loadCatalogs(): void {
		this.api.getCustomers().subscribe({
			next: data => this.customers = data,
			error: err => this.showError(err, 'No se pudieron cargar los clientes.')
		});

		this.api.getEmployees().subscribe({
			next: data => this.employees = data,
			error: err => this.showError(err, 'No se pudieron cargar los empleados.')
		});

		this.api.getProducts().subscribe({
			next: data => this.products = data,
			error: err => this.showError(err, 'No se pudieron cargar los productos.')
		});
	}

	loadOrders(): void {
		this.api.getOrders().subscribe({
			next: data => this.orders = data,
			error: err => this.showError(err, 'No se pudieron cargar las órdenes.')
		});
	}

	createOrder(): void {
		this.error = '';
		this.success = '';

		const product = this.products.find(p => p.product_id === Number(this.form.product_id));

		const data = {
			customer_id: this.form.customer_id,
			employee_id: Number(this.form.employee_id),
			ship_name: this.form.ship_name,
			ship_address: this.form.ship_address,
			ship_city: this.form.ship_city,
			ship_country: this.form.ship_country,
			details: [
				{
					product_id: Number(this.form.product_id),
					unit_price: product?.unit_price || 0,
					quantity: Number(this.form.quantity),
					discount: 0
				}
			]
		};

		this.api.createOrder(data).subscribe({
			next: () => {
				this.success = 'Orden creada correctamente.';
				this.loadOrders();
			},
			error: err => this.showError(err, 'No se pudo crear la orden.')
		});
	}

	private showError(err: any, fallback: string): void {
		console.error(err);
		this.error = err?.error?.error || fallback;
	}
}
