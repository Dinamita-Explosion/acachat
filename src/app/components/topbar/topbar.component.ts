import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="px-4 pt-10 pb-3 mb-2">
      <div class="flex items-center justify-between" style="padding-top: calc(env(safe-area-inset-top) + 8px)">
        <img [src]="logoSrc" alt="Logo" class="h-12 w-12 object-cover" />
        <img [src]="avatarSrc" alt="Perfil" class="h-12 w-12 rounded-full object-cover border-4 border-primary" />
      </div>
    </div>
  `,
})
export class TopbarComponent {
  @Input() logoSrc = 'assets/branding/logo.png';
  @Input() avatarSrc = 'assets/avatars/profile.png';
}
