import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-course-card',
  standalone: true,
  imports: [CommonModule, IonicModule],
  styles: [":host{display:block;width:100%}"],
  template: `
    <ion-button
      mode="ios"
      expand="block"
      fill="solid"
      class="group normal-case justify-start"
      (click)="pressed.emit()"
      [style.--border-radius]="'1.5rem'"
      [style.--padding-start]="'0'"
      [style.--padding-end]="'0'"
      [style.--padding-top]="'0'"
      [style.--padding-bottom]="'0'"
      [style.--background]="gradientCss"
      [style.--background-hover]="gradientCss"
      [style.--background-activated]="gradientCss"
      [style.--border-width]="'1px'"
      [style.--border-color]="'var(--color-brand-100)'"
      [style.--box-shadow]="'0 4px 10px rgba(0,0,0,0.06)'"
    >
      <div class="flex w-full items-center rounded-3xl p-4 text-left">
        <div class="mr-3 flex h-12 w-12 items-center justify-center rounded-full border bg-white text-2xl shadow"
             [ngStyle]="emojiStyle">
          {{ emoji }}
        </div>
        <div class="min-w-0 flex-1">
          <div class="truncate text-base font-semibold text-white">{{ title }}</div>
          <div class="mt-0.5 line-clamp-2 text-sm text-white/90">{{ description }}</div>
          <div class="mt-2 flex items-center gap-3 text-xs text-white/80">
            <div>Profesor: <span class="font-medium text-white">{{ professor }}</span></div>
            <div>Periodo: <span class="font-medium text-white">{{ period }}</span></div>
          </div>
        </div>
      </div>
    </ion-button>
  `,
})
export class CourseCardComponent {
  @Input() emoji = '📘';
  @Input() title = '';
  @Input() description = '';
  @Input() professor = '';
  @Input() period = '';
  @Input() color = '#4a3aff';
  @Output() pressed = new EventEmitter<void>();

  get gradientCss() {
    const c = this.color?.trim() || '#4a3aff';
    if (c.startsWith('#')) {
      const [r, g, b] = this.hexToRgb(c);
      const [dr, dg, db] = this.darkenRgb([r, g, b], 0.18); // 18% darker
      return `linear-gradient(180deg, rgb(${r}, ${g}, ${b}) 0%, rgb(${dr}, ${dg}, ${db}) 100%)`;
    }
    // Fallback for CSS variables: deepen with black, not white
    return `linear-gradient(180deg, ${c} 0%, color-mix(in srgb, ${c} 80%, black) 100%)`;
  }

  get emojiStyle() {
    const c = this.color?.trim() || '#4a3aff';
    if (c.startsWith('#')) {
      const [r, g, b] = this.hexToRgb(c);
      return { borderColor: `rgba(${r}, ${g}, ${b}, 0.5)` } as any;
    }
    return { borderColor: `color-mix(in srgb, ${c} 50%, white)` } as any;
  }

  private hexToRgb(hex: string): [number, number, number] {
    const x = hex.replace('#', '');
    const full = x.length === 3 ? x.split('').map((ch) => ch + ch).join('') : x;
    const r = parseInt(full.substring(0, 2), 16);
    const g = parseInt(full.substring(2, 4), 16);
    const b = parseInt(full.substring(4, 6), 16);
    return [r, g, b];
  }

  private darkenRgb([r, g, b]: [number, number, number], amount: number): [number, number, number] {
    const clamp = (n: number) => Math.max(0, Math.min(255, Math.round(n)));
    return [clamp(r * (1 - amount)), clamp(g * (1 - amount)), clamp(b * (1 - amount))];
  }
}
