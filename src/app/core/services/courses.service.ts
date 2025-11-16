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
  is_active?: boolean;
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

export interface CourseEnrollmentUser {
  id: number;
  username: string;
  email?: string;
  role?: 'student' | 'teacher' | 'admin';
}

export interface CourseEnrollmentWithUser extends CourseEnrollment {
  user?: CourseEnrollmentUser | null;
}

export interface CourseEnrollmentsResponse {
  course: CourseDto;
  enrollments: CourseEnrollmentWithUser[];
  total: number;
}

export interface CourseFileDto {
  id: number;
  filename: string;
  filepath: string;
  filesize: number;
  mimetype: string;
  uploaded_by: number;
  uploaded_at: string | null;
  has_parsed_content?: boolean;
  parsed_at?: string | null;
}

export interface CourseFilesResponse {
  course: {
    id: number;
    nombre: string;
  };
  files: CourseFileDto[];
  total: number;
}

export type CourseUpdatePayload = Partial<{
  nombre: string;
  prompt: string | null;
  emoji: string | null;
  institution_id: number;
  grade_id: number | null;
  is_active: boolean;
}>;

@Injectable({ providedIn: 'root' })
export class CoursesService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  private readonly courses$ = new BehaviorSubject<CourseEnrollment[]>([]);
  private cache: CourseEnrollment[] | null = null;
  private inFlight$: Observable<CourseEnrollment[]> | null = null;
  private requestToken = 0;

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
      const token = ++this.requestToken;
      this.inFlight$ = this.http
        .get<MyCoursesResponse>(`${this.apiBaseUrl}/courses/my-courses`)
        .pipe(
          map((response) => response.enrollments ?? []),
          tap((enrollments) => {
            if (token !== this.requestToken) {
              return;
            }
            this.cache = enrollments;
            this.courses$.next(enrollments);
          }),
          finalize(() => {
            if (token === this.requestToken) {
              this.inFlight$ = null;
            }
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

  clearCache(): void {
    this.requestToken++;
    this.cache = null;
    this.courses$.next([]);
    this.inFlight$ = null;
  }

  uploadCourseFile(courseId: number, file: File) {
    const formData = new FormData();
    formData.append('file', file);

    return this.http
      .post<{ file: CourseFileDto }>(`${this.apiBaseUrl}/courses/${courseId}/files`, formData)
      .pipe(map((response) => response.file));
  }

  getCourseById(courseId: number): Observable<CourseDto> {
    return this.http.get<CourseDto>(`${this.apiBaseUrl}/courses/${courseId}`);
  }

  updateCourse(courseId: number, payload: CourseUpdatePayload): Observable<CourseDto> {
    return this.http
      .put<{ course: CourseDto }>(`${this.apiBaseUrl}/courses/${courseId}`, payload)
      .pipe(map((response) => response.course));
  }

  listCourseFiles(courseId: number): Observable<CourseFilesResponse> {
    return this.http.get<CourseFilesResponse>(`${this.apiBaseUrl}/courses/${courseId}/files`);
  }

  deleteCourseFile(fileId: number): Observable<void> {
    return this.http
      .delete<{ msg?: string }>(`${this.apiBaseUrl}/files/${fileId}`)
      .pipe(map(() => void 0));
  }

  listCourseEnrollments(courseId: number, roleInCourse?: 'student' | 'teacher'): Observable<CourseEnrollmentsResponse> {
    const options = roleInCourse ? { params: { role_in_course: roleInCourse } } : {};
    return this.http.get<CourseEnrollmentsResponse>(`${this.apiBaseUrl}/enrollments/course/${courseId}`, options);
  }
}
