import { Component, inject } from '@angular/core';
import { IonButton, IonContent, IonIcon } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { combineLatest, map } from 'rxjs';
import { TopbarComponent } from '../../components/topbar/topbar.component';
import { CourseCardComponent } from '../../components/course-card/course-card.component';
import { AuthService } from '../../core/services/auth.service';
import { CoursesService, CourseEnrollment } from '../../core/services/courses.service';
import { ThemeService, ThemePalette } from '../../core/services/theme.service';
import { API_BASE_URL } from '../../core/tokens/api.token';
import { buildCourseBadge, buildInitials, resolveUploadedAssetUrl } from '../../core/utils/display.utils';
import { ToastController } from '@ionic/angular';
import { AuthUser } from '../../core/models/auth.models';
import { addIcons } from 'ionicons';
import { cloudUpload } from 'ionicons/icons';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  imports: [CommonModule, IonContent, IonIcon, IonButton, TopbarComponent, CourseCardComponent],
})
export class Tab2Page {
  private readonly auth = inject(AuthService);
  private readonly coursesService = inject(CoursesService);
  private readonly theme = inject(ThemeService);
  private readonly apiBaseUrl = inject(API_BASE_URL);
  private readonly router = inject(Router);
  private readonly toastController = inject(ToastController);

  readonly viewModel$ = combineLatest([
    this.auth.currentUser$,
    this.coursesService.watchMyCourses(),
    this.theme.palette$,
  ]).pipe(
    map(([user, enrollments, palette]) => {
      const initials = buildInitials(user?.username ?? user?.email ?? '');
      const institution = user?.institution ?? null;
      const institutionLogo = resolveUploadedAssetUrl(this.apiBaseUrl, institution?.logotipo ?? null);
      const filtered = this.filterEnrollmentsForUser(user, enrollments);
      const courses = filtered
        .map((enrollment) => this.mapCourse(enrollment, palette))
        .sort((a, b) => a.title.localeCompare(b.title, 'es', { sensitivity: 'base' }));

      return {
        initials,
        institutionLogo,
        palette,
        institutionName: institution?.nombre ?? null,
        courses,
      } satisfies Tab2ViewModel;
    })
  );

  uploadingCourseId: number | null = null;

  constructor() {
    addIcons({ cloudUpload });
    void this.coursesService.loadMyCourses().catch(() => undefined);
  }

  goToProfile() {
    this.router.navigate(['/tabs/profile']);
  }

  onOpenCourse(course: CourseCardView) {
    this.router.navigate(['/chat'], {
      state: {
        title: course.title || 'Chatbot',
        subtitle: course.subtitle || '',
        color: course.color,
        emoji: course.badge,
      },
    });
  }

  private mapCourse(enrollment: CourseEnrollment, palette: ThemePalette): CourseCardView {
    const course = enrollment.course;
    const institution = course?.institution ?? null;
    const color = institution?.colorinstitucional?.trim() || palette.primary;
    const logo = resolveUploadedAssetUrl(this.apiBaseUrl, institution?.logotipo ?? null);
    const badge = course?.emoji ?? buildCourseBadge(course?.nombre ?? '');
    const isTeacher = enrollment.role_in_course === 'teacher';
    const gradeLabel = course?.grade?.name ?? 'Sin grado asignado';
    const institutionName = institution?.nombre ?? 'Sin institución';
    const description = `${gradeLabel} · ${institutionName}`;
    const period = `Año ${enrollment.year}`;

    return {
      id: course?.id ?? enrollment.course_id,
      badge,
      title: course?.nombre ?? 'Curso',
      subtitle: isTeacher ? 'Eres profesor/a del curso' : 'Estudiante del curso',
      description,
      period,
      color,
      logo,
      canUpload: isTeacher,
    };
  }

  onUploadClick(input: HTMLInputElement) {
    input.value = '';
    input.click();
  }

  async onFileSelected(event: Event, course: CourseCardView): Promise<void> {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) {
      return;
    }

    this.uploadingCourseId = course.id;
    this.coursesService.uploadCourseFile(course.id, file).subscribe({
      next: async () => {
        this.uploadingCourseId = null;
        await this.presentToast('Archivo cargado correctamente.', 'success');
        input.value = '';
      },
      error: async (error) => {
        this.uploadingCourseId = null;
        const message = error?.error?.msg ?? 'No se pudo subir el archivo.';
        await this.presentToast(message, 'danger');
        input.value = '';
      },
    });
  }

  private filterEnrollmentsForUser(user: AuthUser | null, enrollments: CourseEnrollment[] | null | undefined): CourseEnrollment[] {
    if (!enrollments) {
      return [];
    }
    if (!user) {
      return enrollments;
    }
    if (user.role === 'teacher') {
      return enrollments.filter((enrollment) => enrollment.role_in_course === 'teacher');
    }
    return enrollments;
  }

  private async presentToast(message: string, color: 'success' | 'danger') {
    const toast = await this.toastController.create({
      message,
      color,
      duration: 2500,
      position: 'bottom',
    });
    await toast.present();
  }
}

interface CourseCardView {
  id: number;
  badge: string;
  title: string;
  subtitle: string;
  description: string;
  period: string;
  color: string;
  logo: string | null;
  canUpload: boolean;
}

interface Tab2ViewModel {
  initials: string;
  institutionLogo: string | null;
  institutionName: string | null;
  palette: ThemePalette;
  courses: CourseCardView[];
}
