import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
	selector: 'app-login',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './login.component.html'
})
export class LoginComponent {
	email = 'admin@cmpg.com';
	password = '123456';
	error = '';
	loading = false;

	constructor(private auth: AuthService, private router: Router) {}

	login(): void {
		this.error = '';
		this.loading = true;

		this.auth.login(this.email, this.password).subscribe({
			next: response => {
				this.auth.saveSession(response);
				this.router.navigate(['/productos']);
			},
			error: err => {
				console.error(err);
				this.error = err?.error?.error || 'No se pudo iniciar sesión.';
				this.loading = false;
			}
		});
	}
}
