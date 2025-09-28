import { Component, inject } from '@angular/core';
import { IonContent, IonIcon } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { addIcons } from 'ionicons';
import { schoolOutline, sunnyOutline, calendarOutline } from 'ionicons/icons';
import { TopbarComponent } from '../../components/topbar/topbar.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  imports: [CommonModule, IonContent, IonIcon, TopbarComponent]
})
export class Tab1Page {
  logoSrc = 'assets/branding/logo.png';
  avatarSrc = 'assets/avatars/profile.png';
  today = new Date();

  private readonly router = inject(Router);

  constructor() {
    addIcons({ schoolOutline, sunnyOutline, calendarOutline });
  }

  goToProfile() {
    this.router.navigate(['/tabs/profile']);
  }
}
