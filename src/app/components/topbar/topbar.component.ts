import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="sticky top-0 z-[15] bg-white px-4 pt-5 pb-3">
      <div class="flex items-center justify-between" style="padding-top: calc(var(--ion-safe-area-top, env(safe-area-inset-top)) + 8px)">
        <img [src]="logoSrc" alt="Logo" class="h-12 w-12 object-cover" />
        <button
          type="button"
          class="h-12 w-12 overflow-hidden rounded-full border-4 border-primary bg-transparent p-0"
          aria-label="Abrir perfil"
          (click)="avatarClicked.emit()"
        >
          <img [src]="avatarSrc" alt="Perfil" class="h-full w-full rounded-full object-cover" />
        </button>
      </div>
      <div class="mt-3 h-px w-full bg-brand-100"></div>
    </div>
  `,
})
export class TopbarComponent {
  @Input() logoSrc = 'assets/branding/logo.png';
  @Input() avatarSrc = 'assets/avatars/profile.png';
  @Output() avatarClicked = new EventEmitter<void>();
}
