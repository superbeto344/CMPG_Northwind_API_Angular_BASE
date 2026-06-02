import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Category } from '../../models/models';

@Component({
	selector: 'app-categorias',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './categorias.component.html'
})
export class CategoriasComponent implements OnInit {
	categories: Category[] = [];
	error = '';
	success = '';
	editingId: number | null = null;

	form: Partial<Category> = {
		category_name: '',
		description: ''
	};

	constructor(private api: ApiService) {}

	ngOnInit(): void {
		this.loadCategories();
	}

	loadCategories(): void {
		this.api.getCategories().subscribe({
			next: data => this.categories = data,
			error: err => this.showError(err, 'No se pudieron cargar las categorías. Revisa Flask.')
		});
	}

	saveCategory(): void {
		this.error = '';
		this.success = '';

		if (!this.form.category_name) {
			this.error = 'El nombre es obligatorio.';
			return;
		}

		if (this.editingId) {
			this.api.updateCategory(this.editingId, this.form).subscribe({
				next: () => {
					this.success = 'Categoría actualizada.';
					this.resetForm();
					this.loadCategories();
				},
				error: err => this.showError(err, 'No se pudo actualizar la categoría.')
			});
			return;
		}

		this.api.createCategory(this.form).subscribe({
			next: () => {
				this.success = 'Categoría creada.';
				this.resetForm();
				this.loadCategories();
			},
			error: err => this.showError(err, 'No se pudo guardar la categoría.')
		});
	}

	editCategory(category: Category): void {
		this.editingId = category.category_id;
		this.form = { ...category };
	}

	deleteCategory(category: Category): void {
		const ok = confirm(`¿Eliminar categoría "${category.category_name}"?`);
		if (!ok) return;

		this.api.deleteCategory(category.category_id).subscribe({
			next: () => {
				this.success = 'Categoría eliminada.';
				this.loadCategories();
			},
			error: err => this.showError(err, 'No se pudo eliminar. Puede tener productos relacionados.')
		});
	}

	resetForm(): void {
		this.editingId = null;
		this.form = {
			category_name: '',
			description: ''
		};
	}

	private showError(err: any, fallback: string): void {
		console.error(err);
		this.error = err?.error?.error || fallback;
	}
}
