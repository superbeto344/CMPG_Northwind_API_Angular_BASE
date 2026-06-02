import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Employee } from '../../models/models';

@Component({
	selector: 'app-empleados',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './empleados.component.html'
})
export class EmpleadosComponent implements OnInit {
	employees: Employee[] = [];
	error = '';

	constructor(private api: ApiService) {}

	ngOnInit(): void {
		this.api.getEmployees().subscribe({
			next: data => this.employees = data,
			error: err => {
				console.error(err);
				this.error = err?.error?.error || 'No se pudieron cargar los empleados.';
			}
		});
	}
}
