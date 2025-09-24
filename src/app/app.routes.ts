import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./welcome/welcome.component').then(m => m.WelcomeComponent),
    pathMatch: 'full',
  },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.routes'),
  },
  {
    path: 'chat',
    loadChildren: () => import('./chat/chat.routes'),
  },
  {
    path: 'tabs',
    loadChildren: () => import('./tabs/tabs.routes'),
  },
];

export default routes;
