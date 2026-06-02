import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Customer } from '../../models/models';

@Component({
	selector: 'app-clientes',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './clientes.component.html'
})
export class ClientesComponent implements OnInit {
	customers: Customer[] = [];
	error = '';

	constructor(private api: ApiService) {}

	ngOnInit(): void {
		this.api.getCustomers().subscribe({
			next: data => this.customers = data,
			error: err => {
				console.error(err);
				this.error = err?.error?.error || 'No se pudieron cargar los clientes.';
			}
		});
	}
}
