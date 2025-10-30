import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

type ButtonVariant = 'primary' | 'secondary' | 'social';

@Component({
  selector: 'app-themed-button',
  standalone: true,
  imports: [CommonModule, IonicModule],
  template: `
    <ion-button
      [type]="type"
      [expand]="expand"
      mode="ios"
      class="font-semibold"
      [disabled]="disabled"
      [style.--background]="background"
      [style.--background-hover]="backgroundHover"
      [style.--background-activated]="backgroundHover"
      [style.--color]="color"
      [style.--color-hover]="color"
      [style.--color-activated]="color"
      [style.--border-radius]="borderRadius"
      [style.--border-width]="borderWidth"
      [style.--border-color]="borderColor"
      [style.--padding-top]="paddingY"
      [style.--padding-bottom]="paddingY"
      [style.--padding-start]="paddingX"
      [style.--padding-end]="paddingX"
      [style.--box-shadow]="boxShadow"
      (click)="clicked.emit($event)">
      <ng-container *ngIf="!iconOnly; else iconOnlyTmpl">
        <ng-content></ng-content>
      </ng-container>
      <ng-template #iconOnlyTmpl>
        <ion-icon
          *ngIf="iconName"
          [name]="assetIconSrc ? undefined : iconName"
          [src]="assetIconSrc"
          slot="icon-only"
          class="text-xl"></ion-icon>
      </ng-template>
    </ion-button>
  `,
})
export class ThemedButtonComponent {
  @Input() variant: ButtonVariant = 'primary';
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() expand: 'block' | 'full' | 'default' = 'block';
  @Input() iconOnly = false;
  @Input() iconName?: string;
  @Input() disabled = false;

  @Output() clicked = new EventEmitter<Event>();

  readonly borderRadius = '0.5rem'; // rounded-lg
  readonly paddingX = '1.25rem';

  get assetIconSrc(): string | undefined {
    if (!this.iconName) {
      return undefined;
    }

    if (this.iconName.includes('/')) {
      return this.iconName.endsWith('.svg') ? this.iconName : `${this.iconName}.svg`;
    }

    if (this.iconName.endsWith('.svg')) {
      return `assets/icon/${this.iconName}`;
    }

    return undefined;
  }

  get paddingY() {
    return this.variant === 'secondary' ? '0.625rem' : '0.75rem';
  }
  get boxShadow() {
    return this.variant === 'primary'
      ? '0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)'
      : 'none';
  }
  get background() {
    switch (this.variant) {
      case 'primary':
        return 'var(--color-primary)';
      case 'secondary':
        return '#fff';
      case 'social':
        return 'var(--color-brand-200)';
    }
  }
  get backgroundHover() {
    switch (this.variant) {
      case 'primary':
        return 'var(--color-primary)';
      case 'secondary':
        return 'var(--color-brand-50)';
      case 'social':
        return 'var(--color-brand-100)';
    }
  }
  get color() {
    switch (this.variant) {
      case 'primary':
        return '#fff';
      case 'secondary':
        return 'var(--color-neutral-800)';
      case 'social':
        return 'var(--color-neutral-800)';
    }
  }
  get borderWidth() {
    return this.variant === 'secondary' ? '1px' : '0';
  }
  get borderColor() {
    return this.variant === 'secondary' ? 'var(--color-brand-100)' : 'transparent';
  }
}
