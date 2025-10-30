import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="sticky top-0 z-[15] bg-white px-4 pt-5 pb-3">
      <div class="flex items-center justify-between gap-4" style="padding-top: calc(var(--ion-safe-area-top, env(safe-area-inset-top)) + 8px)">
        <ng-container *ngIf="logoSrc; else initialsLogo">
          <button
            type="button"
            class="flex items-center justify-center p-0 bg-transparent border-none"
            style="height: 3rem"
            (click)="logoClicked.emit()"
            aria-label="Ver información de la institución"
          >
            <img
              [src]="logoSrc"
              alt="Logo"
              class="h-12 w-auto max-w-[7rem] object-contain"
              decoding="async"
              loading="lazy" />
          </button>
        </ng-container>
        <ng-template #initialsLogo>
          <div class="h-12 w-12 rounded-2xl bg-primary flex items-center justify-center text-white font-semibold text-lg">
            {{ userInitials }}
          </div>
        </ng-template>
        <button
          type="button"
          class="h-12 w-12 rounded-full border-4 border-primary bg-transparent p-0"
          aria-label="Abrir perfil"
          (click)="avatarClicked.emit()"
        >
          <ng-container *ngIf="avatarSrc; else initialsAvatar">
            <img [src]="avatarSrc" alt="Perfil" class="h-full w-full rounded-full object-cover" />
          </ng-container>
          <ng-template #initialsAvatar>
            <div class="h-full w-full flex items-center justify-center rounded-full bg-primary text-white text-lg font-semibold">
              {{ userInitials }}
            </div>
          </ng-template>
        </button>
      </div>
      <div class="mt-3 h-px w-full bg-brand-100"></div>
    </div>
  `,
})
export class TopbarComponent {
  @Input() logoSrc: string | null = null;
  @Input() avatarSrc: string | null = null;
  @Input() userInitials = 'UX';
  @Output() avatarClicked = new EventEmitter<void>();
  @Output() logoClicked = new EventEmitter<void>();
}
