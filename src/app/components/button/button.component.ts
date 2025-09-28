import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg' | 'xl';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  standalone: true,
  imports: [CommonModule],
})
export class ButtonComponent {
  @Input() variant: ButtonVariant = 'primary';
  @Input() size: ButtonSize = 'md';
  @Input() disabled = false;
  @Input() loading = false;
  @Input() fullWidth = false;
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() icon?: string;
  @Input() iconPosition: 'left' | 'right' = 'left';

  @Output() buttonClick = new EventEmitter<Event>();

  onClick(event: Event) {
    if (!this.disabled && !this.loading) {
      this.buttonClick.emit(event);
    }
  }

  get buttonClasses(): string {
    const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

    const variantClasses = {
      primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500',
      secondary: 'bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500',
      outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
      ghost: 'text-blue-600 hover:bg-blue-50 focus:ring-blue-500',
      danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500'
    };

    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm rounded-md',
      md: 'px-4 py-2 text-sm rounded-lg',
      lg: 'px-6 py-3 text-base rounded-lg',
      xl: 'px-8 py-4 text-lg rounded-xl'
    };

    const widthClass = this.fullWidth ? 'w-full' : '';
    const loadingClass = this.loading ? 'cursor-wait' : '';

    return `${baseClasses} ${variantClasses[this.variant]} ${sizeClasses[this.size]} ${widthClass} ${loadingClass}`.trim();
  }
}
