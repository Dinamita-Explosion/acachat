import { Component, inject } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { TopbarComponent } from '../../components/topbar/topbar.component';
import { CourseCardComponent } from '../../components/course-card/course-card.component';

interface CourseSummary {
  emoji: string;
  title: string;
  description: string;
  professor: string;
  period: string;
  color: string;
}

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  imports: [CommonModule, IonContent, TopbarComponent, CourseCardComponent],
})
export class Tab2Page {
  logoSrc = 'assets/branding/logo.png';
  avatarSrc = 'assets/avatars/profile.png';

  private readonly router = inject(Router);

  courses: CourseSummary[] = [
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

  onOpenCourse(course: CourseSummary) {
    // Navega a /chat pasando estado para personalizar el header
    this.router.navigate(['/chat'], {
      state: {
        title: course?.title || 'Chatbot',
        subtitle: course?.professor || '',
        color: course?.color || '#4a3aff',
        emoji: course?.emoji || '🤖',
      },
    });
  }

  goToProfile() {
    this.router.navigate(['/tabs/profile']);
  }
}
