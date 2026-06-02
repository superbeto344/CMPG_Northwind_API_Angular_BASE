import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, Supplier, Product, Customer, Employee, Order, AppUser, LoginResponse } from '../models/models';

@Injectable({
	providedIn: 'root'
})
export class ApiService {
	private baseUrl = 'http://127.0.0.1:5000/api';

	constructor(private http: HttpClient) {}


	login(email: string, password: string): Observable<LoginResponse> {
		return this.http.post<LoginResponse>(`${this.baseUrl}/auth/login`, { email, password });
	}

	registerUser(data: Partial<AppUser> & { password: string }): Observable<AppUser> {
		return this.http.post<AppUser>(`${this.baseUrl}/auth/register`, data);
	}

	getUsers(): Observable<AppUser[]> {
		return this.http.get<AppUser[]>(`${this.baseUrl}/users`);
	}

	getCategories(): Observable<Category[]> {
		return this.http.get<Category[]>(`${this.baseUrl}/categories`);
	}

	createCategory(data: Partial<Category>): Observable<Category> {
		return this.http.post<Category>(`${this.baseUrl}/categories`, data);
	}

	updateCategory(id: number, data: Partial<Category>): Observable<Category> {
		return this.http.put<Category>(`${this.baseUrl}/categories/${id}`, data);
	}

	deleteCategory(id: number): Observable<any> {
		return this.http.delete(`${this.baseUrl}/categories/${id}`);
	}

	getSuppliers(): Observable<Supplier[]> {
		return this.http.get<Supplier[]>(`${this.baseUrl}/suppliers`);
	}

	getProducts(search = '', categoryId = ''): Observable<Product[]> {
		let url = `${this.baseUrl}/products`;
		const params: string[] = [];

		if (search.trim()) {
			params.push(`search=${encodeURIComponent(search.trim())}`);
		}

		if (categoryId) {
			params.push(`category_id=${categoryId}`);
		}

		if (params.length > 0) {
			url += '?' + params.join('&');
		}

		return this.http.get<Product[]>(url);
	}

	createProduct(data: Partial<Product>): Observable<Product> {
		return this.http.post<Product>(`${this.baseUrl}/products`, data);
	}

	updateProduct(id: number, data: Partial<Product>): Observable<Product> {
		return this.http.put<Product>(`${this.baseUrl}/products/${id}`, data);
	}

	deleteProduct(id: number): Observable<any> {
		return this.http.delete(`${this.baseUrl}/products/${id}`);
	}

	getCustomers(): Observable<Customer[]> {
		return this.http.get<Customer[]>(`${this.baseUrl}/customers`);
	}

	getEmployees(): Observable<Employee[]> {
		return this.http.get<Employee[]>(`${this.baseUrl}/employees`);
	}

	getOrders(): Observable<Order[]> {
		return this.http.get<Order[]>(`${this.baseUrl}/orders`);
	}

	createOrder(data: any): Observable<Order> {
		return this.http.post<Order>(`${this.baseUrl}/orders`, data);
	}
}
