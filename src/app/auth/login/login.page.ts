import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  standalone: true,
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    HttpClientModule,
    FormInputComponent,
    ThemedButtonComponent,
    TextTitleComponent,
  ],
})
export class LoginPage {
  email = '';
  password = '';

  private readonly router = inject(Router);
  private readonly http = inject(HttpClient);
  private readonly API_URL = 'http://127.0.0.1:5000'; // URL de tu backend Flask

  onLogin() {
    const loginData = {
      email: this.email,
      password: this.password,
    };

    this.http
      .post<{ access_token: string }>(`${this.API_URL}/api/login`, loginData)
      .pipe(
        tap((response) => {
          console.log('Login exitoso', response);
          // Guardamos el token en el almacenamiento local del navegador
          localStorage.setItem('access_token', response.access_token);
          this.router.navigate(['/tabs/tab1']); // Redirigimos a la página principal
        }),
        catchError((error) => {
          console.error('Error en el login', error);
          // Opcional: Muestra un mensaje de error de "credenciales incorrectas"
          return of(error);
        }),
      )
      .subscribe();
  }

  goToRegister() {
    this.router.navigate(['/auth/register']);
  }
}
