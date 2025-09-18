import { Component } from '@angular/core';
import { IonContent, IonIcon } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { addIcons } from 'ionicons';
import { schoolOutline, sunnyOutline, calendarOutline } from 'ionicons/icons';
import { TopbarComponent } from '../../components/topbar/topbar.component';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  imports: [CommonModule, IonContent, IonIcon, TopbarComponent]
})
export class Tab1Page {
  logoSrc = 'assets/branding/logo.png';
  avatarSrc = 'assets/avatars/profile.png';
  today = new Date();

  constructor() {
    addIcons({ schoolOutline, sunnyOutline, calendarOutline });
  }
}
