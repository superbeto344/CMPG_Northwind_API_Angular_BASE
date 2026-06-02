import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Category, Supplier, Product } from '../../models/models';

@Component({
	selector: 'app-productos',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './productos.component.html'
})
export class ProductosComponent implements OnInit {
	products: Product[] = [];
	categories: Category[] = [];
	suppliers: Supplier[] = [];
	error = '';
	success = '';
	search = '';
	categoryFilter = '';

	form: Partial<Product> = {
		product_name: '',
		supplier_id: 1,
		category_id: 1,
		quantity_per_unit: '',
		unit_price: 0,
		units_in_stock: 0,
		units_on_order: 0,
		reorder_level: 0,
		discontinued: false
	};

	editingId: number | null = null;

	constructor(private api: ApiService) {}

	ngOnInit(): void {
		this.loadCatalogs();
		this.loadProducts();
	}

	loadCatalogs(): void {
		this.api.getCategories().subscribe({
			next: data => this.categories = data,
			error: err => this.showError(err, 'No se pudieron cargar las categorías.')
		});

		this.api.getSuppliers().subscribe({
			next: data => this.suppliers = data,
			error: err => this.showError(err, 'No se pudieron cargar los proveedores.')
		});
	}

	loadProducts(): void {
		this.api.getProducts(this.search, this.categoryFilter).subscribe({
			next: data => this.products = data,
			error: err => this.showError(err, 'No se pudieron cargar los productos. Revisa que Flask esté corriendo.')
		});
	}

	saveProduct(): void {
		this.error = '';
		this.success = '';

		if (!this.form.product_name || !this.form.supplier_id || !this.form.category_id) {
			this.error = 'Nombre, proveedor y categoría son obligatorios.';
			return;
		}

		if (this.editingId) {
			this.api.updateProduct(this.editingId, this.form).subscribe({
				next: () => {
					this.success = 'Producto actualizado correctamente.';
					this.resetForm();
					this.loadProducts();
				},
				error: err => this.showError(err, 'No se pudo actualizar el producto.')
			});
			return;
		}

		this.api.createProduct(this.form).subscribe({
			next: () => {
				this.success = 'Producto creado correctamente.';
				this.resetForm();
				this.loadProducts();
			},
			error: err => this.showError(err, 'No se pudo crear el producto.')
		});
	}

	editProduct(product: Product): void {
		this.editingId = product.product_id;
		this.form = { ...product };
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}

	deleteProduct(product: Product): void {
		const ok = confirm(`¿Eliminar producto "${product.product_name}"?`);
		if (!ok) return;

		this.api.deleteProduct(product.product_id).subscribe({
			next: () => {
				this.success = 'Producto eliminado correctamente.';
				this.loadProducts();
			},
			error: err => this.showError(err, 'No se pudo eliminar. Puede estar relacionado con órdenes.')
		});
	}

	resetForm(): void {
		this.editingId = null;
		this.form = {
			product_name: '',
			supplier_id: this.suppliers[0]?.supplier_id || 1,
			category_id: this.categories[0]?.category_id || 1,
			quantity_per_unit: '',
			unit_price: 0,
			units_in_stock: 0,
			units_on_order: 0,
			reorder_level: 0,
			discontinued: false
		};
	}

	private showError(err: any, fallback: string): void {
		console.error(err);
		this.error = err?.error?.error || fallback;
	}
}
