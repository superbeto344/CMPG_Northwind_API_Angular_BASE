import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter, Routes } from '@angular/router';

import { AppComponent } from './app/app.component';
import { LoginComponent } from './app/components/login/login.component';
import { ProductosComponent } from './app/components/productos/productos.component';
import { CategoriasComponent } from './app/components/categorias/categorias.component';
import { OrdenesComponent } from './app/components/ordenes/ordenes.component';
import { ClientesComponent } from './app/components/clientes/clientes.component';
import { EmpleadosComponent } from './app/components/empleados/empleados.component';
import { UsuariosComponent } from './app/components/usuarios/usuarios.component';
import { authGuard } from './app/services/auth.guard';

const routes: Routes = [
	{ path: 'login', component: LoginComponent },
	{ path: '', redirectTo: 'productos', pathMatch: 'full' },
	{ path: 'productos', component: ProductosComponent, canActivate: [authGuard] },
	{ path: 'categorias', component: CategoriasComponent, canActivate: [authGuard] },
	{ path: 'ordenes', component: OrdenesComponent, canActivate: [authGuard] },
	{ path: 'clientes', component: ClientesComponent, canActivate: [authGuard] },
	{ path: 'empleados', component: EmpleadosComponent, canActivate: [authGuard] },
	{ path: 'usuarios', component: UsuariosComponent, canActivate: [authGuard] },
	{ path: '**', redirectTo: 'productos' }
];

bootstrapApplication(AppComponent, {
	providers: [
		provideHttpClient(),
		provideRouter(routes)
	]
}).catch(err => console.error(err));
