import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'auth',
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
    path: '',
    loadChildren: () => import('./tabs/tabs.routes'),
  },
];

export default routes;
