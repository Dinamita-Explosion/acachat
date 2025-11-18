import { Component, inject } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { NavigationEnd, Router } from '@angular/router';
import { combineLatest, map } from 'rxjs';
import { filter } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { TopbarComponent } from '../../components/topbar/topbar.component';
import { CourseCardComponent } from '../../components/course-card/course-card.component';
import { AuthService } from '../../core/services/auth.service';
import { CoursesService, CourseEnrollment } from '../../core/services/courses.service';
import { ThemeService, ThemePalette } from '../../core/services/theme.service';
import { API_BASE_URL } from '../../core/tokens/api.token';
import { buildCourseBadge, buildInitials, resolveUploadedAssetUrl } from '../../core/utils/display.utils';
import { AuthUser } from '../../core/models/auth.models';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  imports: [CommonModule, IonContent, TopbarComponent, CourseCardComponent],
})
export class Tab2Page {
  private readonly auth = inject(AuthService);
  private readonly coursesService = inject(CoursesService);
  private readonly theme = inject(ThemeService);
  private readonly apiBaseUrl = inject(API_BASE_URL);
  private readonly router = inject(Router);

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
        .map((enrollment) => this.mapCourse(enrollment, palette, user))
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

  constructor() {
    this.refreshCourses(false);
    this.router.events
      .pipe(
        filter((event): event is NavigationEnd => event instanceof NavigationEnd),
        filter((event) => event.urlAfterRedirects.startsWith('/tabs/tab2')),
        takeUntilDestroyed(),
      )
      .subscribe(() => this.refreshCourses(true));
  }

  goToProfile() {
    this.router.navigate(['/tabs/profile']);
  }

  onOpenCourse(course: CourseCardView) {
    this.router.navigate(['/chat'], {
      state: {
        courseId: course.id,
        title: course.title || 'Chatbot',
        subtitle: course.subtitle || '',
        color: course.color,
        emoji: course.badge,
        canManage: course.canManage,
      },
    });
  }

  private mapCourse(enrollment: CourseEnrollment, palette: ThemePalette, user: AuthUser | null): CourseCardView {
    const course = enrollment.course;
    const institution = course?.institution ?? null;
    const isTeacher = enrollment.role_in_course === 'teacher';
    const chatHiddenForStudents = course?.chat_hidden_for_students === true;
    const isStudentUser = user?.role === 'student';
    const isDisabledForUser = chatHiddenForStudents && (isStudentUser || isTeacher);
    const color = isDisabledForUser ? '#cbd5f5' : institution?.colorinstitucional?.trim() || palette.primary;
    const logo = resolveUploadedAssetUrl(this.apiBaseUrl, institution?.logotipo ?? null);
    const badge = course?.emoji ?? buildCourseBadge(course?.nombre ?? '');
    const isAdmin = user?.role === 'admin';
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
      canManage: Boolean(isTeacher || isAdmin),
    };
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

  private refreshCourses(force: boolean): void {
    void this.coursesService.loadMyCourses(force).catch(() => undefined);
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
  canManage: boolean;
}

interface Tab2ViewModel {
  initials: string;
  institutionLogo: string | null;
  institutionName: string | null;
  palette: ThemePalette;
  courses: CourseCardView[];
}
