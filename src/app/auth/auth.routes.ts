import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./login/login.page').then(m => m.LoginPage)
  },
  {
    path: 'register',
    loadComponent: () => import('./register/register.page').then(m => m.RegisterPage)
  },
  {
    path: 'change-password',
    loadComponent: () => import('./change-password/change-password.page').then(m => m.ChangePasswordPage)
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  }
];

export default routes;
