export interface Category {
	category_id: number;
	category_name: string;
	description?: string;
}

export interface Supplier {
	supplier_id: number;
	company_name: string;
	contact_name?: string;
	phone?: string;
	country?: string;
}

export interface Product {
	product_id: number;
	product_name: string;
	supplier_id: number;
	supplier_name?: string;
	category_id: number;
	category_name?: string;
	quantity_per_unit?: string;
	unit_price: number;
	units_in_stock: number;
	units_on_order?: number;
	reorder_level?: number;
	discontinued: boolean;
}

export interface Customer {
	customer_id: string;
	company_name: string;
	contact_name?: string;
	city?: string;
	country?: string;
}

export interface Employee {
	employee_id: number;
	first_name: string;
	last_name: string;
	full_name: string;
	title?: string;
}

export interface OrderDetail {
	product_id: number;
	product_name?: string;
	unit_price: number;
	quantity: number;
	discount: number;
	subtotal?: number;
}

export interface Order {
	order_id: number;
	customer_id: string;
	customer_name?: string;
	employee_id: number;
	employee_name?: string;
	order_date?: string;
	ship_name?: string;
	ship_city?: string;
	ship_country?: string;
	total?: number;
	details?: OrderDetail[];
}


export interface AppUser {
	user_id: number;
	full_name: string;
	email: string;
	role: string;
	status: string;
}

export interface LoginResponse {
	message: string;
	token: string;
	user: AppUser;
}
