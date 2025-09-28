 import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-legal-modal',
  standalone: true,
  imports: [CommonModule, IonicModule, HttpClientModule],
  template: `
    <ion-modal
      mode="ios"
      [isOpen]="isOpen"
      (didDismiss)="onDismiss()"
      style="
        --width: min(92vw, 428px);
        --max-width: 428px;
        --height: 80vh;
        --border-radius: 16px;
        --background: #fff;
      "
    >
      <ng-template>
        <ion-content class="bg-white">
          <div class="relative h-full">
            <ion-button
              fill="clear"
              mode="ios"
              class="absolute left-4 top-0 z-10 m-0 h-9 w-9 -translate-y-1/2 rounded-full shadow"
              [style.--border-radius]="'9999px'"
              [style.--background]="'var(--color-neutral-300)'"
              [style.--color]="'var(--color-neutral-800)'"
              (click)="onDismiss()"
            >
              <ion-icon name="chevron-back" slot="icon-only"></ion-icon>
            </ion-button>

            <div class="flex h-full flex-col">
              <div class="flex items-center justify-center border-b border-brand-100 px-5 py-4">
                <h2 class="text-base font-semibold text-primary">{{ title }}</h2>
              </div>

              <div class="min-h-0 flex-1 overflow-auto p-4">
                <div class="space-y-4 text-sm text-neutral-800" [innerHTML]="html"></div>
              </div>
            </div>
          </div>
        </ion-content>
      </ng-template>
    </ion-modal>
  `,
})
export class LegalModalComponent implements OnChanges {
  @Input() isOpen = false;
  @Input() title = '';
  @Input() src = '';
  @Output() closed = new EventEmitter<void>();

  html = '<p>Cargando…</p>';

  constructor(private http: HttpClient) {}

  ngOnChanges(changes: SimpleChanges): void {
    if ((changes['isOpen'] || changes['src']) && this.isOpen && this.src) {
      this.loadContent();
    }
  }

  private loadContent() {
    this.html = '<p>Cargando…</p>';
    this.http
      .get(this.src, { responseType: 'text' })
      .subscribe({
        next: (text) => (this.html = text || '<p>Sin contenido</p>'),
        error: () => (this.html = '<p>No se pudo cargar el contenido.</p>'),
      });
  }

  onDismiss() {
    this.closed.emit();
  }
}
