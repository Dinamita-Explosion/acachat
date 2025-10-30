import { DOCUMENT } from '@angular/common';
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface ThemePalette {
  primary: string;
  primaryRgb: string;
  contrast: string;
  contrastRgb: string;
  shade: string;
  tint: string;
  muted: string;
  mutedContrast: string;
}

interface RgbColor {
  r: number;
  g: number;
  b: number;
}

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private readonly document = inject(DOCUMENT);
  private readonly defaultColor = '#4a3aff';

  private readonly paletteSubject = new BehaviorSubject<ThemePalette>(this.buildPalette(this.defaultColor));

  readonly palette$ = this.paletteSubject.asObservable();

  constructor() {
    this.applyCssVariables(this.paletteSubject.value);
  }

  applyPrimaryColor(color: string | null | undefined): void {
    const normalized = this.normalizeHex(color) ?? this.defaultColor;
    const palette = this.buildPalette(normalized);
    const current = this.paletteSubject.value;
    if (this.arePalettesEqual(current, palette)) {
      return;
    }

    this.paletteSubject.next(palette);
    this.applyCssVariables(palette);
  }

  private arePalettesEqual(a: ThemePalette, b: ThemePalette): boolean {
    return (
      a.primary === b.primary &&
      a.contrast === b.contrast &&
      a.shade === b.shade &&
      a.tint === b.tint &&
      a.muted === b.muted &&
      a.mutedContrast === b.mutedContrast
    );
  }

  private normalizeHex(color: string | null | undefined): string | null {
    if (!color) {
      return null;
    }
    const trimmed = color.trim();
    if (!trimmed) {
      return null;
    }

    const hex = trimmed.startsWith('#') ? trimmed : `#${trimmed}`;
    const match = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(hex);
    if (!match) {
      return null;
    }
    const value = match[1];
    if (value.length === 3) {
      const expanded = value.split('').map((c) => c + c).join('');
      return `#${expanded.toLowerCase()}`;
    }
    return `#${value.toLowerCase()}`;
  }

  private buildPalette(primaryHex: string): ThemePalette {
    const primaryRgb = this.hexToRgb(primaryHex) ?? this.hexToRgb(this.defaultColor)!;

    const contrast = this.chooseContrast(primaryRgb);
    const shade = this.mix(primaryRgb, { r: 0, g: 0, b: 0 }, 0.18);
    const tint = this.mix(primaryRgb, { r: 255, g: 255, b: 255 }, 0.16);
    const muted = this.mix(primaryRgb, { r: 255, g: 255, b: 255 }, 0.72);
    const mutedContrast = this.chooseContrast(muted);

    return {
      primary: primaryHex,
      primaryRgb: this.rgbToString(primaryRgb),
      contrast: contrast.hex,
      contrastRgb: this.rgbToString(contrast.rgb),
      shade: this.rgbToHex(shade),
      tint: this.rgbToHex(tint),
      muted: this.rgbToHex(muted),
      mutedContrast: mutedContrast.hex,
    };
  }

  private applyCssVariables(palette: ThemePalette): void {
    const root = this.document.documentElement;

    root.style.setProperty('--color-primary', palette.primary);
    root.style.setProperty('--color-secondary', palette.primary);

    root.style.setProperty('--ion-color-primary', palette.primary);
    root.style.setProperty('--ion-color-primary-rgb', palette.primaryRgb);
    root.style.setProperty('--ion-color-primary-contrast', palette.contrast);
    root.style.setProperty('--ion-color-primary-contrast-rgb', palette.contrastRgb);
    root.style.setProperty('--ion-color-primary-shade', palette.shade);
    root.style.setProperty('--ion-color-primary-tint', palette.tint);

    root.style.setProperty('--app-primary-contrast', palette.contrast);
    root.style.setProperty('--app-primary-muted', palette.muted);
    root.style.setProperty('--app-primary-muted-contrast', palette.mutedContrast);
  }

  private hexToRgb(hex: string): RgbColor | null {
    const match = /^#([0-9a-f]{6})$/i.exec(hex);
    if (!match) {
      return null;
    }
    const value = match[1];
    return {
      r: parseInt(value.slice(0, 2), 16),
      g: parseInt(value.slice(2, 4), 16),
      b: parseInt(value.slice(4, 6), 16),
    };
  }

  private rgbToHex({ r, g, b }: RgbColor): string {
    const toHex = (component: number) => this.clamp(component).toString(16).padStart(2, '0');
    return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
  }

  private rgbToString({ r, g, b }: RgbColor): string {
    return `${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)}`;
  }

  private clamp(value: number): number {
    return Math.max(0, Math.min(255, Math.round(value)));
  }

  private mix(source: RgbColor, target: RgbColor, weight: number): RgbColor {
    const w = Math.max(0, Math.min(1, weight));
    return {
      r: source.r * (1 - w) + target.r * w,
      g: source.g * (1 - w) + target.g * w,
      b: source.b * (1 - w) + target.b * w,
    };
  }

  private chooseContrast(color: RgbColor): { hex: string; rgb: RgbColor } {
    const luminance = this.relativeLuminance(color);
    const dark: RgbColor = { r: 17, g: 15, b: 73 }; // #110f49
    const light: RgbColor = { r: 255, g: 255, b: 255 };
    const chosen = luminance > 0.6 ? dark : light;
    return { hex: this.rgbToHex(chosen), rgb: chosen };
  }

  private relativeLuminance({ r, g, b }: RgbColor): number {
    const srgb = [r, g, b].map((value) => {
      const channel = value / 255;
      return channel <= 0.03928 ? channel / 12.92 : Math.pow((channel + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2];
  }
}
