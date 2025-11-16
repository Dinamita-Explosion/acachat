import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { finalize } from 'rxjs/operators';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';
import { AuthService } from '../../core/services/auth.service';
import { ChangePasswordRequest } from '../../core/models/auth.models';
import { extractErrorMessage } from '../../core/utils/http-error.utils';
import { validateEmail, validatePassword } from '../../core/utils/form-validators';

@Component({
  selector: 'app-change-password',
  standalone: true,
  templateUrl: './change-password.page.html',
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
    FormInputComponent,
    ThemedButtonComponent,
    TextTitleComponent,
  ],
})
export class ChangePasswordPage {
  email = '';
  currentPassword = '';
  newPassword = '';
  confirmNewPassword = '';
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  private readonly router = inject(Router);
  private readonly auth = inject(AuthService);

  onSubmit() {
    this.errorMessage = '';
    this.successMessage = '';

    const validationError = this.validateForm();
    if (validationError) {
      this.errorMessage = validationError;
      return;
    }

    const payload: ChangePasswordRequest = {
      email: this.email.trim().toLowerCase(),
      old_password: this.currentPassword,
      new_password: this.newPassword,
    };

    this.isLoading = true;

    this.auth
      .changePassword(payload)
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response) => {
          this.successMessage = response?.msg ?? 'Contraseña actualizada correctamente.';
          this.currentPassword = '';
          this.newPassword = '';
          this.confirmNewPassword = '';
        },
        error: (error) => {
          this.errorMessage = extractErrorMessage(error) || 'No se pudo actualizar la contraseña. Intenta nuevamente.';
          console.error('Error al cambiar contraseña', error);
        },
      });
  }

  goToLogin() {
    this.router.navigate(['/auth/login']);
  }

  private validateForm(): string | null {
    const email = this.email.trim();
    if (!email) {
      return 'El email es obligatorio.';
    }
    if (!validateEmail(email)) {
      return 'Ingresa un email válido.';
    }
    if (!this.currentPassword.trim()) {
      return 'Debes ingresar tu contraseña actual.';
    }
    const passwordError = validatePassword(this.newPassword);
    if (passwordError) {
      return passwordError;
    }
    if (this.newPassword === this.currentPassword) {
      return 'La nueva contraseña debe ser diferente a la actual.';
    }
    if (!this.confirmNewPassword.trim()) {
      return 'Debes confirmar la nueva contraseña.';
    }
    if (this.newPassword !== this.confirmNewPassword) {
      return 'La confirmación de la nueva contraseña no coincide.';
    }
    return null;
  }
}
