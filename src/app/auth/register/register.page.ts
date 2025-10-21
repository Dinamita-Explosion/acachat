import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { FormSelectComponent, SelectOption } from '../../components/form-select/form-select.component';
import { LegalModalComponent } from '../../components/legal-modal/legal-modal.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  standalone: true,
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    HttpClientModule,
    FormInputComponent,
    FormSelectComponent,
    ThemedButtonComponent,
    TextTitleComponent,
    LegalModalComponent,
  ],
})
export class RegisterPage {
  username = '';
  rut = '';
  email = '';
  region = '';
  comuna = '';
  password = '';
  confirmPassword = '';

  acceptTerms = false;

  regions: SelectOption<string>[] = [
    { label: 'Región Metropolitana', value: 'RM' },
    { label: 'Valparaíso', value: 'V' },
    { label: 'Biobío', value: 'VIII' },
  ];

  comunasByRegion: Record<string, SelectOption<string>[]> = {
    RM: [
      { label: 'Santiago', value: 'santiago' },
      { label: 'Providencia', value: 'providencia' },
      { label: 'Las Condes', value: 'las-condes' },
    ],
    V: [
      { label: 'Valparaíso', value: 'valparaiso' },
      { label: 'Viña del Mar', value: 'vina-del-mar' },
    ],
    VIII: [
      { label: 'Concepción', value: 'concepcion' },
      { label: 'Talcahuano', value: 'talcahuano' },
    ],
  };

  private readonly router = inject(Router);
  private readonly http = inject(HttpClient);
  private readonly API_URL = 'http://127.0.0.1:5000'; // URL de tu backend Flask

  onRegister() {
    if (!this.acceptTerms) {
      console.warn('Debe aceptar términos y condiciones.');
      // Aquí podrías mostrar una alerta al usuario
      return;
    }
    if (this.password !== this.confirmPassword) {
      console.warn('Las contraseñas no coinciden');
      // Aquí podrías mostrar una alerta al usuario
      return;
    }

    const registerData = {
      username: this.username,
      rut: this.rut,
      email: this.email,
      region: this.region,
      comuna: this.comuna,
      password: this.password,
    };

    this.http
      .post(`${this.API_URL}/api/register`, registerData)
      .pipe(
        tap((response) => {
          console.log('Registro exitoso', response);
          // Opcional: Muestra un mensaje de éxito
          this.router.navigate(['/auth/login']); // Redirige a login después del registro
        }),
        catchError((error) => {
          console.error('Error en el registro', error);
          // Opcional: Muestra un mensaje de error al usuario
          return of(error); // Continúa el flujo de manera controlada
        }),
      )
      .subscribe();
  }

  goToLogin() {
    this.router.navigate(['/auth/login']);
  }

  get comunas(): SelectOption<string>[] {
    return this.comunasByRegion[this.region] ?? [];
  }

  isTermsOpen = false;
  isPrivacyOpen = false;
}
