import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';
import { ButtonComponent } from '../../components/button/button.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule, ButtonComponent],
})
export class LoginPage {
  email: string = '';
  password: string = '';

  constructor(private router: Router) {}

  async onLogin() {
    console.log('Login attempt:', { email: this.email, password: this.password });
  }

  goToRegister() {
    this.router.navigate(['/auth/register']);
  }
}