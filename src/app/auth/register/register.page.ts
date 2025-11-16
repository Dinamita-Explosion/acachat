import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { FormSelectComponent, SelectOption } from '../../components/form-select/form-select.component';
import { LegalModalComponent } from '../../components/legal-modal/legal-modal.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';
import { finalize } from 'rxjs/operators';
import { AuthService } from '../../core/services/auth.service';
import { RegisterRequest } from '../../core/models/auth.models';
import { environment } from '../../../environments/environment';
import { validateEmail, validatePassword, validateRut } from '../../core/utils/form-validators';
import { extractErrorMessage } from '../../core/utils/http-error.utils';

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
export class RegisterPage implements OnInit {
  username = '';
  rut = '';
  email = '';
  region = '';
  comuna = '';
  password = '';
  confirmPassword = '';
  institutionId: string | null = null;

  acceptTerms = false;
  isLoading = false;
  isLoadingInstitutions = false;
  errorMessage = '';

  institutions: SelectOption<string>[] = [];

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
  private readonly auth = inject(AuthService);
  private readonly http = inject(HttpClient);

  ngOnInit() {
    this.loadInstitutions();
  }

  loadInstitutions() {
    this.isLoadingInstitutions = true;
    this.http
      .get<InstitutionApiResponse>(`${environment.apiBaseUrl}/institutions?per_page=100`)
      .pipe(finalize(() => (this.isLoadingInstitutions = false)))
      .subscribe({
        next: (response) => {
          this.institutions = response.institutions.map((inst) => ({
            label: inst.nombre,
            value: String(inst.id),
          }));
        },
        error: (error) => {
          console.error('Error loading institutions', error);
          this.errorMessage = 'Error al cargar las instituciones. Intenta de nuevo.';
        },
      });
  }

  onRegister() {
    this.errorMessage = '';

    const validationError = this.validateForm();
    if (validationError) {
      this.errorMessage = validationError;
      return;
    }

    const registerData = {
      username: this.username.trim(),
      rut: this.rut.trim(),
      email: this.email.trim().toLowerCase(),
      region: this.region,
      comuna: this.comuna,
      password: this.password,
      institution_id: Number(this.institutionId),
      role: 'student',
    } satisfies RegisterRequest;

    this.isLoading = true;
    this.errorMessage = '';

    this.auth
      .register(registerData)
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response) => {
          console.log('Registro exitoso', response);
          this.router.navigate(['/auth/login']);
        },
        error: (error) => {
          this.errorMessage = extractErrorMessage(error) || 'Error al registrar usuario';
          console.error('Error en el registro', error);
        },
      });
  }

  goToLogin() {
    this.router.navigate(['/auth/login']);
  }

  private validateForm(): string | null {
    const username = this.username.trim();
    if (!username) {
      return 'El nombre de usuario es obligatorio.';
    }
    if (username.length < 3 || username.length > 80) {
      return 'El nombre de usuario debe tener entre 3 y 80 caracteres.';
    }

    const rut = this.rut.trim();
    if (!rut) {
      return 'El RUT es obligatorio.';
    }
    if (!validateRut(rut)) {
      return 'El RUT ingresado no es válido.';
    }

    const email = this.email.trim();
    if (!email) {
      return 'El correo electrónico es obligatorio.';
    }
    if (!validateEmail(email)) {
      return 'Ingresa un correo electrónico válido.';
    }

    if (!this.institutionId) {
      return 'Debes seleccionar una institución.';
    }

    if (!this.region) {
      return 'Selecciona una región.';
    }

    if (!this.comuna) {
      return 'Selecciona una comuna.';
    }

    const passwordError = validatePassword(this.password);
    if (passwordError) {
      return passwordError;
    }

    if (!this.confirmPassword.trim()) {
      return 'Debes confirmar tu contraseña.';
    }

    if (this.password !== this.confirmPassword) {
      return 'Las contraseñas no coinciden.';
    }

    if (!this.acceptTerms) {
      return 'Debes aceptar los términos y condiciones para continuar.';
    }

    return null;
  }

  get comunas(): SelectOption<string>[] {
    return this.comunasByRegion[this.region] ?? [];
  }

  isTermsOpen = false;
  isPrivacyOpen = false;
}

interface InstitutionApiResponse {
  institutions: InstitutionApiModel[];
}

interface InstitutionApiModel {
  id: number;
  nombre: string;
}
