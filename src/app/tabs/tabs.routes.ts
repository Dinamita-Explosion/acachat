import { Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

export const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'tab1',
        loadChildren: () => import('../home/tab1/tab1.routes'),
      },
      {
        path: 'tab2',
        loadChildren: () => import('../home/tab2/tab2.routes'),
      },
      {
        path: 'profile',
        loadChildren: () => import('../profile/profile.routes'),
      },
      {
        path: '',
        redirectTo: '/tabs/tab1',
        pathMatch: 'full',
      },
    ],
  },
];

export default routes;
