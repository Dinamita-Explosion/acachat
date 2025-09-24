import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent } from '@ionic/angular/standalone';
import { Router } from '@angular/router';
import { TextTitleComponent } from '../components/text-title/text-title.component';
import { ThemedButtonComponent } from '../components/themed-button/themed-button.component';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  standalone: true,
  imports: [CommonModule, IonContent, TextTitleComponent, ThemedButtonComponent],
})
export class WelcomeComponent {

  constructor(private router: Router) {}

  goToLogin() {
    this.router.navigate(['/auth/login']);
  }

  goToRegister() {
    this.router.navigate(['/auth/register']);
  }
}