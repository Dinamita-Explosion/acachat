import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="px-4 pt-5 pb-3">
      <div class="flex items-center justify-between" style="padding-top: calc(var(--ion-safe-area-top, env(safe-area-inset-top)) + 8px)">
        <img [src]="logoSrc" alt="Logo" class="h-12 w-12 object-cover" />
        <img [src]="avatarSrc" alt="Perfil" class="h-12 w-12 rounded-full object-cover border-4 border-primary" />
      </div>
      <div class="mt-3 h-px w-full bg-brand-100"></div>
    </div>
  `,
})
export class TopbarComponent {
  @Input() logoSrc = 'assets/branding/logo.png';
  @Input() avatarSrc = 'assets/avatars/profile.png';
}
