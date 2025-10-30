import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';
import { finalize } from 'rxjs/operators';
import { AuthService } from '../../core/services/auth.service';
import { LoginRequest } from '../../core/models/auth.models';

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
  isLoading = false;
  errorMessage = '';

  private readonly router = inject(Router);
  private readonly auth = inject(AuthService);

  onLogin() {
    const loginData = {
      email: this.email,
      password: this.password,
    } satisfies LoginRequest;

    this.isLoading = true;
    this.errorMessage = '';

    this.auth
      .login(loginData)
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: () => {
          this.router.navigate(['/tabs/tab1']);
        },
        error: (error) => {
          this.errorMessage = extractErrorMessage(error) || 'Error al iniciar sesión. Verifica tus credenciales.';
          console.error('Error en el login', error);
        },
      });
  }

  goToRegister() {
    this.router.navigate(['/auth/register']);
  }
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
