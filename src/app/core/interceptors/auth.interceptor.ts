import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

const AUTH_HEADER = 'Authorization';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const token = auth.getAccessToken();
  const shouldAttachToken = Boolean(token) && !request.headers.has(AUTH_HEADER);

  const authReq = shouldAttachToken
    ? request.clone({
        setHeaders: {
          [AUTH_HEADER]: `Bearer ${token}`,
        },
      })
    : request;

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && token) {
        auth.logout();

        const currentUrl = router.url ?? '';
        if (!currentUrl.startsWith('/auth')) {
          void router.navigate(['/auth/login']);
        }
      }
      return throwError(() => error);
    }),
  );
};
