import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

const AUTH_HEADER = 'Authorization';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);
  const token = auth.getAccessToken();

  if (!token || request.headers.has(AUTH_HEADER)) {
    return next(request);
  }

  const authReq = request.clone({
    setHeaders: {
      [AUTH_HEADER]: `Bearer ${token}`,
    },
  });

  return next(authReq);
};
