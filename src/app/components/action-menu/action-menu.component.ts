import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { IonPopover, IonIcon } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { chevronForward } from 'ionicons/icons';

type ActionIntent = 'default' | 'destructive';

export interface ActionMenuItem {
  label: string;
  icon?: string;
  intent?: ActionIntent;
  id: string;
}

@Component({
  selector: 'app-action-menu',
  standalone: true,
  imports: [CommonModule, IonPopover, IonIcon],
  template: `
    <ion-popover
      [isOpen]="isOpen"
      [event]="event"
      (didDismiss)="dismiss.emit()"
      mode="ios"
      size="auto"
      class="action-menu"
    >
      <ng-template>
        <div class="min-w-[200px] space-y-1 p-2">
          <button
            *ngFor="let action of actions"
            type="button"
            class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm"
            [ngClass]="action.intent === 'destructive' ? 'text-red-600 hover:bg-red-50' : 'text-neutral-900 hover:bg-brand-50'"
            (click)="actionSelected.emit(action.id)"
          >
            <span class="flex items-center gap-2">
              <ion-icon *ngIf="action.icon" [name]="action.icon" class="text-base"></ion-icon>
              {{ action.label }}
            </span>
            <ion-icon name="chevron-forward" class="text-xs text-neutral-400"></ion-icon>
          </button>
        </div>
      </ng-template>
    </ion-popover>
  `,
  styles: [
    `
      :host ::ng-deep .action-menu {
        --background: #fff;
        --box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
        border-radius: 16px;
        overflow: hidden;
      }
    `,
  ],
})
export class ActionMenuComponent {
  @Input() isOpen = false;
  @Input() event?: Event;
  @Input() actions: ActionMenuItem[] = [];

  @Output() dismiss = new EventEmitter<void>();
  @Output() actionSelected = new EventEmitter<string>();

  constructor() {
    addIcons({ chevronForward });
  }
}
