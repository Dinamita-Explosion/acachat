import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, firstValueFrom } from 'rxjs';
import { finalize, map, shareReplay, tap } from 'rxjs/operators';
import { API_BASE_URL } from '../tokens/api.token';

export interface CourseInstitution {
  id: number;
  nombre: string;
  colorinstitucional?: string | null;
  logotipo?: string | null;
}

export interface CourseGrade {
  id: number;
  name: string;
  order: number;
}

export interface CourseDto {
  id: number;
  nombre: string;
  prompt?: string | null;
  institution_id: number;
  grade_id: number | null;
  institution?: CourseInstitution | null;
  grade?: CourseGrade | null;
  teachers_count?: number;
  students_count?: number;
  files_count?: number;
  emoji?: string | null;
}

export interface CourseEnrollment {
  id: number;
  user_id: number;
  course_id: number;
  year: number;
  role_in_course: 'student' | 'teacher';
  enrolled_at: string | null;
  course?: CourseDto | null;
}

interface MyCoursesResponse {
  enrollments: CourseEnrollment[];
}

export interface CourseFileDto {
  id: number;
  filename: string;
  filepath: string;
  filesize: number;
  mimetype: string;
  uploaded_by: number;
  uploaded_at: string | null;
}

@Injectable({ providedIn: 'root' })
export class CoursesService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  private readonly courses$ = new BehaviorSubject<CourseEnrollment[]>([]);
  private cache: CourseEnrollment[] | null = null;
  private inFlight$: Observable<CourseEnrollment[]> | null = null;

  /**
   * Devuelve un observable con la lista de cursos del usuario actual.
   * Si aún no se han cargado, se disparará automáticamente la carga inicial.
   */
  watchMyCourses(): Observable<CourseEnrollment[]> {
    if (!this.cache) {
      void this.loadMyCourses();
    }
    return this.courses$.asObservable();
  }

  /**
   * Fuerza la recarga de los cursos del usuario.
   */
  loadMyCourses(force = false): Promise<CourseEnrollment[]> {
    if (this.cache && !force) {
      return Promise.resolve(this.cache);
    }

    if (!this.inFlight$) {
      this.inFlight$ = this.http
        .get<MyCoursesResponse>(`${this.apiBaseUrl}/courses/my-courses`)
        .pipe(
          map((response) => response.enrollments ?? []),
          tap((enrollments) => {
            this.cache = enrollments;
            this.courses$.next(enrollments);
          }),
          finalize(() => {
            this.inFlight$ = null;
          }),
          shareReplay(1),
        );
    }

    return this.inFlight$
      ? firstValueFrom(this.inFlight$)
      : Promise.resolve(this.cache ?? []);
  }

  /**
   * Permite actualizar la caché localmente (p.ej. después de editar un curso).
   */
  setMyCourses(enrollments: CourseEnrollment[]): void {
    this.cache = enrollments;
    this.courses$.next(enrollments);
  }

  uploadCourseFile(courseId: number, file: File) {
    const formData = new FormData();
    formData.append('file', file);

    return this.http
      .post<{ file: CourseFileDto }>(`${this.apiBaseUrl}/courses/${courseId}/files`, formData)
      .pipe(map((response) => response.file));
  }
}
