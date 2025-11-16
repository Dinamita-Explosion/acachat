import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonContent, IonIcon } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { personCircleOutline, schoolOutline, businessOutline } from 'ionicons/icons';
import { Router } from '@angular/router';
import { ScreenHeaderComponent } from '../components/screen-header/screen-header.component';
import { AuthService } from '../core/services/auth.service';
import { ThemeService, ThemePalette } from '../core/services/theme.service';
import { API_BASE_URL } from '../core/tokens/api.token';
import { buildInitials, resolveUploadedAssetUrl } from '../core/utils/display.utils';
import { extractErrorMessage } from '../core/utils/http-error.utils';
import { combineLatest, firstValueFrom, map } from 'rxjs';
import { AuthUser } from '../core/models/auth.models';
import { AlertController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-profile',
  standalone: true,
  templateUrl: './profile.page.html',
  imports: [CommonModule, IonContent, IonIcon, ScreenHeaderComponent],
})
export class ProfilePage {
  private readonly router = inject(Router);
  private readonly auth = inject(AuthService);
  private readonly theme = inject(ThemeService);
  private readonly apiBaseUrl = inject(API_BASE_URL);
  private readonly alertController = inject(AlertController);
  private readonly toastController = inject(ToastController);

  readonly viewModel$ = combineLatest([this.auth.currentUser$, this.theme.palette$]).pipe(
    map(([user, palette]) => this.buildViewModel(user, palette)),
  );

  constructor() {
    addIcons({ personCircleOutline, schoolOutline, businessOutline });
  }

  goBack(): void {
    this.router.navigate(['/tabs/tab1']);
  }

  async onSettings(): Promise<void> {
    const user = await firstValueFrom(this.auth.currentUser$);
    if (!user) {
      await this.presentToast('No hay sesión activa.', 'danger');
      return;
    }

    const alert = await this.alertController.create({
      header: 'Editar nombre',
      message: 'Solo puedes actualizar tu nombre de usuario.',
      inputs: [
        {
          name: 'username',
          type: 'text',
          value: user.username,
          attributes: {
            maxlength: 80,
            autocapitalize: 'words',
          },
        },
      ],
      buttons: [
        {
          text: 'Cerrar sesión',
          role: 'destructive',
          handler: () => {
            void this.handleLogout(alert);
            return false;
          },
        },
        {
          text: 'Cancelar',
          role: 'cancel',
        },
        {
          text: 'Guardar',
          handler: (data) => {
            const username = (data?.username ?? '').trim();
            void this.handleNameUpdate(alert, username, user);
            return false; // evitar cerrar automáticamente
          },
        },
      ],
    });

    await alert.present();
  }

  private buildViewModel(user: AuthUser | null, palette: ThemePalette): ProfileViewModel {
    const initials = buildInitials(user?.username ?? user?.email ?? '');
    const institution = user?.institution ?? null;
    const institutionLogo = resolveUploadedAssetUrl(this.apiBaseUrl, institution?.logotipo ?? null);
    const location = buildLocation(user);
    const gradeName = user?.grade?.name ?? 'Sin grado asignado';

    return {
      user,
      palette,
      initials,
      institutionLogo,
      institutionName: institution?.nombre ?? 'Sin institución asignada',
      location,
      gradeName,
    };
  }

  private async handleNameUpdate(alert: HTMLIonAlertElement, username: string, user: AuthUser): Promise<void> {
    if (!username) {
      await this.presentToast('El nombre no puede estar vacío.', 'warning');
      return;
    }

    if (username === user.username) {
      await alert.dismiss();
      return;
    }

    try {
      await firstValueFrom(this.auth.updateProfile({ username }));
      await alert.dismiss();
      await this.presentToast('Nombre actualizado correctamente.', 'success');
    } catch (error) {
      const message = extractErrorMessage(error) ?? 'No se pudo actualizar el nombre.';
      await this.presentToast(message, 'danger');
    }
  }

  private async handleLogout(alert: HTMLIonAlertElement): Promise<void> {
    await alert.dismiss();
    this.auth.logout();
    await this.presentToast('Sesión cerrada.', 'success');
    await this.router.navigate(['/auth/login']);
  }

  private async presentToast(message: string, color: 'success' | 'warning' | 'danger'): Promise<void> {
    const toast = await this.toastController.create({
      message,
      color,
      duration: 2500,
      position: 'top',
      buttons: [{ text: 'Cerrar', role: 'cancel' }],
    });
    await toast.present();
  }
}

interface ProfileViewModel {
  user: AuthUser | null;
  palette: ThemePalette;
  initials: string;
  institutionName: string;
  institutionLogo: string | null;
  location: string;
  gradeName: string;
}

function buildLocation(user: AuthUser | null): string {
  if (!user) {
    return 'Ubicación no disponible';
  }
  const parts = [user.comuna, user.region].filter(Boolean);
  return parts.length ? parts.join(', ') : 'Ubicación no disponible';
}
