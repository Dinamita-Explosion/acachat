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
      .get<{ institutions: any[] }>(`${environment.apiBaseUrl}/institutions?per_page=100`)
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
    if (!this.acceptTerms) {
      this.errorMessage = 'Debes aceptar los términos y condiciones para continuar.';
      return;
    }
    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Las contraseñas no coinciden';
      return;
    }
    if (!this.institutionId) {
      this.errorMessage = 'Debes seleccionar una institución';
      return;
    }

    const registerData = {
      username: this.username,
      rut: this.rut,
      email: this.email,
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

  get comunas(): SelectOption<string>[] {
    return this.comunasByRegion[this.region] ?? [];
  }

  isTermsOpen = false;
  isPrivacyOpen = false;
}

function extractErrorMessage(error: unknown): string | null {
  if (!error) return null;
  const err: any = error;
  const raw = err?.error?.msg ?? err?.message ?? err?.statusText;
  if (!raw) return null;
  if (typeof raw === 'string') {
    return normalizeErrorString(raw);
  }
  if (Array.isArray(raw)) {
    return raw.map(item => (typeof item === 'string' ? item : JSON.stringify(item))).join(' ');
  }
  if (typeof raw === 'object') {
    return Object.values(raw)
      .flat()
      .map((item) => (typeof item === 'string' ? item : JSON.stringify(item)))
      .join(' ');
  }
  return null;
}

function normalizeErrorString(message: string): string {
  const trimmed = message.trim();
  if (!trimmed.startsWith('{') || !trimmed.endsWith('}')) {
    return trimmed;
  }
  try {
    const parsed = JSON.parse(
      trimmed
        .replace(/'/g, '"')
        .replace(/None/g, 'null')
        .replace(/True/g, 'true')
        .replace(/False/g, 'false'),
    );
    return Object.values(parsed)
      .flat()
      .map((item: unknown) => (typeof item === 'string' ? item : JSON.stringify(item)))
      .join(' ');
  } catch {
    return trimmed;
  }
}
