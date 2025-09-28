import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent, IonIcon } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { personCircleOutline, schoolOutline, businessOutline } from 'ionicons/icons';
import { Router } from '@angular/router';
import { ScreenHeaderComponent } from '../components/screen-header/screen-header.component';

@Component({
  selector: 'app-profile',
  standalone: true,
  templateUrl: './profile.page.html',
  imports: [CommonModule, IonContent, IonIcon, ScreenHeaderComponent],
})
export class ProfilePage {
  name = 'Nicolás Pérez';
  course = '1° Medio A';
  courseDescription = 'Plan Científico Humanista';
  institution = 'Colegio del Daniel';
  institutionLocation = 'Quillota, Chile';
  avatarSrc = 'assets/avatars/profile.png';
  institutionLogo = 'assets/branding/logo.png';

  constructor(private router: Router) {
    addIcons({ personCircleOutline, schoolOutline, businessOutline });
  }

  goBack() {
    this.router.navigate(['/tabs/tab1']);
  }

  onSettings() {}
}
