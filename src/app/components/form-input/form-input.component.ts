import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NG_VALUE_ACCESSOR, ControlValueAccessor, FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-form-input',
  standalone: true,
  imports: [CommonModule, FormsModule, IonicModule],
  styles: [
    `:host{display:block;width:100%;}`
  ],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => FormInputComponent),
      multi: true,
    },
  ],
  template: `
    <label class="block">
      <span class="sr-only">{{ placeholder }}</span>
      <div
        class="flex items-center gap-2 rounded-lg bg-neutral-300 px-3 py-3 ring-0 transition-shadow focus-within:ring-2 focus-within:ring-primary sm:px-4">
        <ion-icon *ngIf="icon" [name]="icon" class="text-neutral-700"></ion-icon>
        <input
          [attr.type]="type"
          [attr.name]="name"
          [attr.autocomplete]="autocomplete"
          [attr.placeholder]="placeholder"
          [disabled]="disabled"
          [required]="required"
          class="w-full bg-transparent text-base font-medium text-neutral-700 placeholder:text-neutral-700 focus:outline-none"
          [value]="value"
          (input)="onInput($event)"
          (blur)="onTouched()"
        />
      </div>
    </label>
  `,
})
export class FormInputComponent implements ControlValueAccessor {
  @Input() type: HTMLInputElement['type'] = 'text';
  @Input() name?: string;
  @Input() placeholder = '';
  @Input() icon?: string;
  @Input() autocomplete?: string;
  @Input() required = false;
  @Input() disabled = false;

  value = '';

  private onChange: (val: string) => void = () => undefined;
  onTouched: () => void = () => undefined;

  writeValue(value: string | null | undefined): void {
    this.value = value ?? '';
  }
  registerOnChange(fn: (value: string) => void): void {
    this.onChange = fn;
  }
  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }
  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }

  onInput(event: Event) {
    const target = event.target as HTMLInputElement;
    this.value = target.value;
    this.onChange(this.value);
  }
}
