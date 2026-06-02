import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from './api.service';
import { AppUser, LoginResponse } from '../models/models';

@Injectable({
	providedIn: 'root'
})
export class AuthService {
	private tokenKey = 'cmpg_token';
	private userKey = 'cmpg_user';

	constructor(private api: ApiService, private router: Router) {}

	login(email: string, password: string) {
		return this.api.login(email, password);
	}

	saveSession(response: LoginResponse): void {
		localStorage.setItem(this.tokenKey, response.token);
		localStorage.setItem(this.userKey, JSON.stringify(response.user));
	}

	logout(): void {
		localStorage.removeItem(this.tokenKey);
		localStorage.removeItem(this.userKey);
		this.router.navigate(['/login']);
	}

	isLoggedIn(): boolean {
		return !!localStorage.getItem(this.tokenKey);
	}

	getUser(): AppUser | null {
		const raw = localStorage.getItem(this.userKey);
		return raw ? JSON.parse(raw) as AppUser : null;
	}
}
