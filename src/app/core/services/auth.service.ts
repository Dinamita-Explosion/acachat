import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap, map, throwError } from 'rxjs';
import { API_BASE_URL } from '../tokens/api.token';
import { ThemeService } from './theme.service';
import { AuthUser, LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, StoredSession } from '../models/auth.models';

const STORAGE_KEY = 'acachat.auth.session';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);
  private readonly theme = inject(ThemeService);
  private readonly session$ = new BehaviorSubject<StoredSession | null>(this.readSession());

  /** Observable con el usuario autenticado */
  readonly currentUser$ = this.session$.pipe(map(session => session?.user ?? null));

  constructor() {
    const session = this.session$.value;
    this.theme.applyPrimaryColor(session?.user?.institution?.colorinstitucional ?? null);
  }

  login(payload: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiBaseUrl}/auth/login`, payload).pipe(
      tap(response => {
        this.persistSession({
          tokens: {
            accessToken: response.access_token,
            refreshToken: response.refresh_token,
          },
          user: response.user,
        });
      }),
    );
  }

  register(payload: RegisterRequest): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${this.apiBaseUrl}/auth/register`, payload);
  }

  updateProfile(changes: { username: string }): Observable<AuthUser> {
    const session = this.session$.value;
    if (!session) {
      return throwError(() => new Error('No hay sesión activa'));
    }

    return this.http.patch<{ user: AuthUser }>(`${this.apiBaseUrl}/auth/profile`, changes).pipe(
      map((response) => response.user),
      tap((user) => this.updateStoredUser(user)),
    );
  }

  logout(): void {
    localStorage.removeItem(STORAGE_KEY);
    this.session$.next(null);
    this.theme.applyPrimaryColor(null);
  }

  getAccessToken(): string | null {
    return this.session$.value?.tokens.accessToken ?? null;
  }

  getRefreshToken(): string | null {
    return this.session$.value?.tokens.refreshToken ?? null;
  }

  getCurrentUser(): AuthUser | null {
    return this.session$.value?.user ?? null;
  }

  private persistSession(session: StoredSession): void {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    this.session$.next(session);
    this.theme.applyPrimaryColor(session.user?.institution?.colorinstitucional ?? null);
  }

  private updateStoredUser(user: AuthUser): void {
    const session = this.session$.value;
    if (!session) {
      return;
    }
    const updated: StoredSession = {
      tokens: session.tokens,
      user,
    };
    this.persistSession(updated);
  }

  private readSession(): StoredSession | null {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as StoredSession;
    } catch {
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }
  }
}
