import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NG_VALUE_ACCESSOR, ControlValueAccessor, FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

export interface SelectOption<T = string> {
  label: string;
  value: T;
}

@Component({
  selector: 'app-form-select',
  standalone: true,
  imports: [CommonModule, FormsModule, IonicModule],
  styles: [':host{display:block;width:100%;}'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => FormSelectComponent),
      multi: true,
    },
  ],
  template: `
    <label class="block">
      <span class="sr-only">{{ placeholder }}</span>
      <div
        class="flex items-center gap-2 rounded-lg bg-neutral-300 px-3 py-3 ring-0 transition-shadow focus-within:ring-2 focus-within:ring-primary sm:px-4">
        <ion-icon *ngIf="icon" [name]="icon" class="text-neutral-700"></ion-icon>
        <select
          class="w-full bg-transparent text-base font-medium text-neutral-700 focus:outline-none"
          [disabled]="disabled"
          [required]="required"
          [name]="name"
          [value]="value"
          (change)="onChangeSelect($event)"
          (blur)="onTouched()">
          <option value="" disabled selected hidden>{{ placeholder }}</option>
          <option *ngFor="let opt of options" [value]="opt.value">{{ opt.label }}</option>
        </select>
        <ion-icon name="chevron-down-outline" class="text-neutral-700"></ion-icon>
      </div>
    </label>
  `,
})
export class FormSelectComponent implements ControlValueAccessor {
  @Input() name?: string;
  @Input() placeholder = '';
  @Input() icon?: string;
  @Input() required = false;
  @Input() disabled = false;
  @Input() options: SelectOption[] = [];

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

  onChangeSelect(event: Event) {
    const target = event.target as HTMLSelectElement;
    this.value = target.value;
    this.onChange(this.value);
  }
}
