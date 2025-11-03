import { Component, inject } from '@angular/core';
import { IonContent, IonIcon } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { addIcons } from 'ionicons';
import { schoolOutline, sunnyOutline, calendarOutline } from 'ionicons/icons';
import { TopbarComponent } from '../../components/topbar/topbar.component';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { combineLatest, Observable } from 'rxjs';
import { distinctUntilChanged, map } from 'rxjs/operators';
import { AuthUser } from '../../core/models/auth.models';
import { ThemePalette, ThemeService } from '../../core/services/theme.service';
import { API_BASE_URL } from '../../core/tokens/api.token';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { buildInitials, resolveUploadedAssetUrl } from '../../core/utils/display.utils';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  imports: [CommonModule, IonContent, IonIcon, TopbarComponent]
})
export class Tab1Page {
  today = new Date();
  private readonly router = inject(Router);
  private readonly auth = inject(AuthService);
  private readonly theme = inject(ThemeService);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  readonly currentUser$: Observable<AuthUser | null> = this.auth.currentUser$;
  readonly viewModel$ = combineLatest([this.currentUser$, this.theme.palette$]).pipe(
    map(([user, palette]) => {
      const initials = buildInitials(user?.username ?? user?.email ?? '');
      const institution = user?.institution ?? null;
      const gradeName = user?.grade?.name ?? 'Sin grado asignado';
      const institutionAddress = institution?.direccion || 'Dirección no disponible';
      const institutionWebsite = institution?.paginaweb || null;
      return {
        user,
        initials,
        institutionName: institution?.nombre ?? null,
        institutionLogo: this.resolveInstitutionLogo(institution?.logotipo ?? null),
        palette,
        gradeName,
        institutionAddress,
        institutionWebsite,
      } satisfies Tab1ViewModel;
    })
  );

  constructor() {
    addIcons({ schoolOutline, sunnyOutline, calendarOutline });
    this.currentUser$
      .pipe(
        map(user => user?.institution?.colorinstitucional ?? null),
        distinctUntilChanged(),
        takeUntilDestroyed()
      )
      .subscribe(color => this.theme.applyPrimaryColor(color));
  }

  goToProfile() {
    this.router.navigate(['/tabs/profile']);
  }

  openInstitutionInfo(vm: Tab1ViewModel): void {
    const lines = [
      vm.institutionName ? `Institución: ${vm.institutionName}` : null,
      vm.institutionAddress ? `Dirección: ${vm.institutionAddress}` : null,
      vm.institutionWebsite ? `Sitio web: ${vm.institutionWebsite}` : null,
    ].filter((value): value is string => Boolean(value));

    const message = lines.length ? lines.join('\n') : 'Sin datos institucionales disponibles.';
    window.alert(message);
  }
  
  private resolveInstitutionLogo(path: string | null | undefined): string | null {
    return resolveUploadedAssetUrl(this.apiBaseUrl, path ?? null);
  }
}

interface Tab1ViewModel {
  user: AuthUser | null;
  initials: string;
  institutionName: string | null;
  institutionLogo: string | null;
  palette: ThemePalette;
  gradeName: string;
  institutionAddress: string;
  institutionWebsite: string | null;
}
