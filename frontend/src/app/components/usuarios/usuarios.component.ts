import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { AppUser } from '../../models/models';

@Component({
	selector: 'app-usuarios',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './usuarios.component.html'
})
export class UsuariosComponent implements OnInit {
	users: AppUser[] = [];
	error = '';

	constructor(private api: ApiService) {}

	ngOnInit(): void {
		this.api.getUsers().subscribe({
			next: data => this.users = data,
			error: err => {
				console.error(err);
				this.error = err?.error?.error || 'No se pudieron cargar los usuarios.';
			}
		});
	}
}
