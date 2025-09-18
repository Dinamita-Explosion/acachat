import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { FormSelectComponent, SelectOption } from '../../components/form-select/form-select.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';
import { LegalModalComponent } from '../../components/legal-modal/legal-modal.component';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  standalone: true,
  imports: [
    IonicModule,
    CommonModule,
    FormsModule,
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

  constructor(private router: Router) {}

  async onRegister() {
    if (!this.acceptTerms) {
      console.warn('Debe aceptar términos y condiciones.');
      return;
    }
    if (this.password !== this.confirmPassword) {
      console.warn('Las contraseñas no coinciden');
      return;
    }
    console.log('Register attempt:', {
      username: this.username,
      rut: this.rut,
      email: this.email,
      region: this.region,
      comuna: this.comuna,
      password: this.password,
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
