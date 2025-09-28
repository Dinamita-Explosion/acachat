import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-text-title',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h1 class="text-2xl font-bold text-primary sm:text-3xl text-center">{{ text }}</h1>
  `,
})
export class TextTitleComponent {
  @Input() text = '';
}
