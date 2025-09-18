import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';
import { FormInputComponent } from '../../components/form-input/form-input.component';
import { ThemedButtonComponent } from '../../components/themed-button/themed-button.component';
import { TextTitleComponent } from '../../components/text-title/text-title.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, FormInputComponent, ThemedButtonComponent, TextTitleComponent],
})
export class LoginPage {
  email = '';
  password = '';

  constructor(private router: Router) {}

  async onLogin() {
    this.router.navigate(['/tabs/tab1']);
  }

  goToRegister() {
    this.router.navigate(['/auth/register']);
  }
}
