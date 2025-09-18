import { Component } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { TopbarComponent } from '../../components/topbar/topbar.component';
import { CourseCardComponent } from '../../components/course-card/course-card.component';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  imports: [CommonModule, IonContent, TopbarComponent, CourseCardComponent],
})
export class Tab2Page {
  logoSrc = 'assets/branding/logo.png';
  avatarSrc = 'assets/avatars/profile.png';

  courses = [
    {
      emoji: '🧮',
      title: 'Matemáticas I',
      description: 'Álgebra básica, ecuaciones y funciones.',
      professor: 'M. Pérez',
      period: 'Sem 1 · 2025',
      color: '#4a3aff',
    },
    {
      emoji: '📚',
      title: 'Lenguaje y Comunicación sdsdsdsd',
      description: 'Comprensión lectora y redacción.',
      professor: 'L. Ramírez',
      period: 'Sem 1 · 2025',
      color: '#ff0000',
    },
    {
      emoji: '🧪',
      title: 'Física',
      description: 'Cinemática y dinámica.',
      professor: 'C. Soto',
      period: 'Sem 1 · 2025',
      color: '#f59e0b',
    },
    {
      emoji: '🏛️',
      title: 'Historia',
      description: 'Historia de Chile contemporánea.',
      professor: 'P. Fuentes',
      period: 'Sem 1 · 2025',
      color: '#ef4444',
    },
  ];

  onOpenCourse(course: any) {
    console.log('Abrir curso:', course);
    // TODO: Navegar al detalle del curso cuando exista la ruta
  }
}
