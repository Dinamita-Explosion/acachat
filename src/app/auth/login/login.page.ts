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
import { validateEmail, validatePassword } from '../../core/utils/form-validators';
import { extractErrorMessage } from '../../core/utils/http-error.utils';

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
    this.errorMessage = '';

    const validationError = this.validateForm();
    if (validationError) {
      this.errorMessage = validationError;
      return;
    }

    const loginData = {
      email: this.email.trim(),
      password: this.password,
    } satisfies LoginRequest;

    this.isLoading = true;

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

  goToChangePassword() {
    this.router.navigate(['/auth/change-password']);
  }

  private validateForm(): string | null {
    const email = this.email.trim();
    if (!email) {
      return 'El email es obligatorio.';
    }
    if (!validateEmail(email)) {
      return 'Ingresa un email válido.';
    }

    const passwordError = validatePassword(this.password, { enforceComplexity: false });
    if (passwordError) {
      return passwordError;
    }

    return null;
  }
}
