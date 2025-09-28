import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { IonButton, IonHeader, IonIcon, IonToolbar } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { chevronBack, ellipsisHorizontal, settingsOutline } from 'ionicons/icons';

@Component({
  selector: 'app-screen-header',
  standalone: true,
  imports: [CommonModule, IonHeader, IonToolbar, IonButton, IonIcon],
  template: `
    <ion-header [translucent]="false" class="bg-white no-shadow">
      <ion-toolbar
        class="bg-white"
        style="--background:#fff; --border-color: var(--color-brand-100); --border-width: 0 0 1px 0; box-shadow:none; -webkit-box-shadow:none;"
      >
        <div class="px-4 pt-5 pb-3">
          <div class="flex w-full items-center gap-3">
            <ion-button
              *ngIf="showBackButton"
              fill="clear"
              class="m-0 h-9 w-9 rounded-full bg-[color:var(--color-neutral-300)] text-neutral-800"
              type="button"
              (click)="back.emit($event)"
              [attr.aria-label]="backAriaLabel"
            >
              <ion-icon [name]="backIcon" slot="icon-only"></ion-icon>
            </ion-button>

            <span
              *ngIf="showTitleBlock && emoji"
              class="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-base"
              [style.background]="accentColor"
              [style.color]="'#fff'"
            >
              {{ emoji }}
            </span>

            <div
              *ngIf="showTitleBlock && (title || subtitle)"
              class="flex min-w-0 flex-1 flex-col leading-tight"
            >
              <span *ngIf="title" class="truncate text-[16px] font-semibold text-neutral-900">{{ title }}</span>
              <span *ngIf="subtitle" class="truncate text-[11px] text-brand-700">{{ subtitle }}</span>
            </div>

            <ion-button
              *ngIf="showActionButton"
              fill="clear"
              class="ml-auto m-0 h-9 w-9 rounded-full bg-[color:var(--color-neutral-300)] text-neutral-800"
              type="button"
              (click)="action.emit($event)"
              [attr.aria-label]="actionAriaLabel"
            >
              <ion-icon [name]="actionIcon" slot="icon-only"></ion-icon>
            </ion-button>
          </div>
        </div>
      </ion-toolbar>
    </ion-header>
  `,
})
export class ScreenHeaderComponent {
  @Input() title = '';
  @Input() subtitle?: string;
  @Input() emoji?: string;
  @Input() accentColor = 'var(--color-primary)';
  @Input() backIcon = 'chevron-back';
  @Input() backAriaLabel = 'Volver';
  @Input() showBackButton = true;
  @Input() showActionButton = false;
  @Input() actionIcon = 'ellipsis-horizontal';
  @Input() actionAriaLabel = 'Más opciones';
  @Input() showTitleBlock = true;

  @Output() back = new EventEmitter<Event>();
  @Output() action = new EventEmitter<Event>();

  constructor() {
    addIcons({ chevronBack, ellipsisHorizontal, settingsOutline });
  }
}
