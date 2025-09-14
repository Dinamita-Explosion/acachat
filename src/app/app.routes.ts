import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.routes'),
  },
  {
    path: '',
    loadChildren: () => import('./tabs/tabs.routes'),
  },
];

export default routes;
