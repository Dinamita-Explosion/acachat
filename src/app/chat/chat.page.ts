import { Component, inject } from '@angular/core';
import { IonButton, IonContent, IonFooter, IonIcon, IonInput, IonModal } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { addIcons } from 'ionicons';
import { send, trashOutline, ellipsisHorizontal, chevronBack, downloadOutline, copyOutline, settingsOutline, cloudUpload, saveOutline } from 'ionicons/icons';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { NavController } from '@ionic/angular';
import { ActionMenuComponent, ActionMenuItem } from '../components/action-menu/action-menu.component';
import { ScreenHeaderComponent } from '../components/screen-header/screen-header.component';
import { ChatService, CourseChatMessage } from '../core/services/chat.service';
import { CoursesService, CourseFileDto } from '../core/services/courses.service';
import { AuthService } from '../core/services/auth.service';
import { firstValueFrom } from 'rxjs';

interface ChatMessage {
  id: number;
  from: 'user' | 'bot';
  text: string;
  time: string;
  meta?: boolean; // not sent to LLM
}

type ChatNavKey = 'title' | 'subtitle' | 'color' | 'emoji';

@Component({
  selector: 'app-chat',
  templateUrl: 'chat.page.html',
  imports: [
    CommonModule,
    FormsModule,
    ScreenHeaderComponent,
    ActionMenuComponent,
    IonButton,
    IonContent,
    IonFooter,
    IonIcon,
    IonInput,
    IonModal,
  ],
})
export class ChatPage {

  messages: ChatMessage[] = [
    { id: 1, from: 'bot', text: 'Nueva conversación iniciada. ¿En qué te ayudo?', time: this.now(), meta: true },
  ];

  draft = '';
  isSending = false;
  temperature = 0.6;
  maxOutputTokens = 2048;
  private readonly sanitizer = inject(DomSanitizer);
  private readonly router = inject(Router);
  private readonly nav = inject(NavController);
  private readonly chatService = inject(ChatService);
  private readonly auth = inject(AuthService);
  private readonly coursesService = inject(CoursesService);

  // Header props (populated from navigation state)
  headerTitle = 'Chatbot';
  headerSubtitle?: string;
  headerColor = 'var(--color-primary)';
  headerEmoji = '🤖';
  isOptionsOpen = false;
  optionsEvent?: Event;
  chatStartedAt = new Date();
  chatStartedDisplay = this.formatChatStart(this.chatStartedAt);
  courseId: number | null = null;
  canManageCourse = false;

  menuActions: ActionMenuItem[] = [];

  // Configuración del curso
  isConfigOpen = false;
  isConfigLoading = false;
  configError: string | null = null;
  promptDraft = '';
  originalPrompt = '';
  isSavingPrompt = false;
  promptSaveMessage: string | null = null;
  filesMessage: string | null = null;
  files: CourseFileDto[] = [];
  isFilesLoading = false;
  isUploadingFile = false;
  uploadError: string | null = null;
  isDeletingFileId: number | null = null;
  courseConfigName: string | null = null;

  constructor() {
    addIcons({ send, trashOutline, ellipsisHorizontal, chevronBack, downloadOutline, copyOutline, settingsOutline, cloudUpload, saveOutline });

    const state = (this.router.getCurrentNavigation()?.extras?.state ??
      window.history.state) as Record<string, unknown> | undefined;

    if (state) {
      this.headerTitle = this.readNavStateValue(state, 'title') ?? this.headerTitle;
      this.headerSubtitle = this.readNavStateValue(state, 'subtitle') ?? this.headerSubtitle;
      this.headerColor = this.readNavStateValue(state, 'color') ?? this.headerColor;
      this.headerEmoji = this.readNavStateValue(state, 'emoji') ?? this.headerEmoji;
      this.courseId = this.readNavStateNumber(state, 'courseId');
      this.canManageCourse = Boolean(state['canManage']);
    }

    const currentUser = this.auth.getCurrentUser();

    if (currentUser?.role === 'admin') {
      this.canManageCourse = true;
    } else if (currentUser?.role !== 'teacher') {
      // Estudiantes u otros roles no pueden gestionar el curso aunque el estado previo lo indique.
      this.canManageCourse = false;
    }

    this.buildMenuActions();
  }

  openOptions(event: Event) {
    this.optionsEvent = event;
    this.isOptionsOpen = true;
  }

  closeOptions() {
    this.isOptionsOpen = false;
    this.optionsEvent = undefined;
  }

  handleMenuSelection(actionId: string) {
    switch (actionId) {
      case 'download':
        this.downloadChat();
        break;
      case 'copy':
        this.copyChat();
        break;
      case 'configure':
        this.openConfiguration();
        break;
      default:
        this.closeOptions();
    }
  }

  copyChat() {
    const text = this.formatChatForExport();
    const clipboard = navigator?.clipboard;
    if (clipboard?.writeText) {
      clipboard
        .writeText(text)
        .then(() => this.closeOptions())
        .catch(() => this.closeOptions());
    } else {
      this.closeOptions();
    }
  }

  downloadChat() {
    const text = this.formatChatForExport();
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'chat.txt';
    anchor.click();
    URL.revokeObjectURL(url);
    this.closeOptions();
  }

  private buildMenuActions() {
    const actions: ActionMenuItem[] = [
      { id: 'download', label: 'Descargar conversación', icon: 'download-outline' },
      { id: 'copy', label: 'Copiar conversación', icon: 'copy-outline' },
    ];
    if (this.canManageCourse) {
      actions.push({ id: 'configure', label: 'Configurar curso', icon: 'settings-outline' });
    }
    this.menuActions = actions;
  }

  openConfiguration() {
    if (!this.canManageCourse) {
      this.closeOptions();
      return;
    }
    this.closeOptions();
    this.isConfigOpen = true;
    this.filesMessage = null;
    this.promptSaveMessage = null;
    void this.loadCourseConfiguration();
  }

  closeConfiguration() {
    this.isConfigOpen = false;
  }

  private async loadCourseConfiguration(): Promise<void> {
    if (!this.courseId) {
      this.configError = 'No se pudo determinar el curso.';
      this.isConfigLoading = false;
      return;
    }

    this.isConfigLoading = true;
    this.isFilesLoading = true;
    this.configError = null;

    try {
      const [course, filesResponse] = await Promise.all([
        firstValueFrom(this.coursesService.getCourseById(this.courseId)),
        firstValueFrom(this.coursesService.listCourseFiles(this.courseId)),
      ]);

      this.courseConfigName = course.nombre;
      this.promptDraft = course.prompt ?? '';
      this.originalPrompt = this.promptDraft;
      this.files = filesResponse.files ?? [];
    } catch (error) {
      console.error('Error al cargar configuración del curso', error);
      this.configError = this.resolveErrorMessage(error, 'No se pudo cargar la configuración del curso.');
    } finally {
      this.isConfigLoading = false;
      this.isFilesLoading = false;
    }
  }

  savePrompt() {
    if (!this.courseId || this.isSavingPrompt) {
      return;
    }

    const payloadPrompt = this.promptDraft?.trim() ? this.promptDraft.trim() : null;

    if (payloadPrompt === (this.originalPrompt?.trim() || null)) {
      this.promptSaveMessage = 'No hay cambios para guardar.';
      return;
    }

    this.isSavingPrompt = true;
    this.promptSaveMessage = null;
    this.configError = null;

    this.coursesService.updateCourse(this.courseId, { prompt: payloadPrompt }).subscribe({
      next: (course) => {
        this.originalPrompt = course.prompt ?? '';
        this.promptDraft = course.prompt ?? '';
        this.promptSaveMessage = 'Prompt actualizado correctamente.';
        this.isSavingPrompt = false;
      },
      error: (error) => {
        console.error('Error al actualizar prompt', error);
        this.configError = this.resolveErrorMessage(error, 'No se pudo actualizar el prompt.');
        this.isSavingPrompt = false;
      },
    });
  }

  onConfigFileSelected(event: Event) {
    if (!this.courseId || this.isUploadingFile) {
      return;
    }

    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) {
      return;
    }

    this.isUploadingFile = true;
    this.uploadError = null;
    this.filesMessage = null;

    this.coursesService.uploadCourseFile(this.courseId, file).subscribe({
      next: async () => {
        this.isUploadingFile = false;
        this.filesMessage = 'Archivo subido correctamente.';
        input.value = '';
        await this.refreshFiles();
      },
      error: async (error) => {
        console.error('Error al subir archivo', error);
        this.uploadError = this.resolveErrorMessage(error, 'No se pudo subir el archivo.');
        this.isUploadingFile = false;
        input.value = '';
        await this.refreshFiles();
      },
    });
  }

  deleteFile(fileId: number) {
    if (this.isDeletingFileId !== null) {
      return;
    }

    this.isDeletingFileId = fileId;
    this.uploadError = null;
    this.filesMessage = null;

    this.coursesService.deleteCourseFile(fileId).subscribe({
      next: async () => {
        this.isDeletingFileId = null;
        this.filesMessage = 'Archivo eliminado correctamente.';
        await this.refreshFiles();
      },
      error: (error) => {
        console.error('Error al eliminar archivo', error);
        this.uploadError = this.resolveErrorMessage(error, 'No se pudo eliminar el archivo.');
        this.isDeletingFileId = null;
      },
    });
  }

  private async refreshFiles() {
    if (!this.courseId) {
      return;
    }
    this.isFilesLoading = true;
    try {
      const response = await firstValueFrom(this.coursesService.listCourseFiles(this.courseId));
      this.files = response.files ?? [];
    } catch (error) {
      console.error('Error al refrescar archivos', error);
      this.uploadError = this.resolveErrorMessage(error, 'No se pudo actualizar la lista de archivos.');
    } finally {
      this.isFilesLoading = false;
    }
  }

  handleBack() {
    try {
      // Si hay historial, vuelve. Si no, navega a Tab2 por defecto
      if (window.history.length > 1) {
        this.nav.back();
      } else {
        this.router.navigate(['/tabs/tab2']);
      }
    } catch {
      this.router.navigate(['/tabs/tab2']);
    }
  }

  sendMessage() {
    if (this.isSending) return;
    const text = this.draft?.trim();
    if (!text) return;
    this.messages = [
      ...this.messages,
      { id: Date.now(), from: 'user', text, time: this.now() },
    ];
    this.draft = '';
    const botId = Date.now() + 1;
    this.messages = [
      ...this.messages,
      { id: botId, from: 'bot', text: '', time: this.now() },
    ];
    this.sendCourseChatRequest(botId);
  }

  clearChat() {
    this.messages = [
      { id: Date.now(), from: 'bot', text: 'Nueva conversación iniciada. ¿En qué te ayudo?', time: this.now() },
    ];
  }

  private now() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  private sendCourseChatRequest(botId: number) {
    if (!this.courseId) {
      console.error('No se pudo determinar el curso para el chat.');
      this.updateBotText(botId, '\n\n[Error] No se logró identificar el curso. Vuelve a abrirlo desde la lista.');
      return;
    }

    const payloadMessages = this.buildBackendMessages();
    if (payloadMessages.length === 0) {
      this.updateBotText(botId, 'No tengo mensajes para procesar.');
      return;
    }

    this.isSending = true;
    this.chatService
      .sendCourseMessage(this.courseId, {
        messages: payloadMessages,
        temperature: this.temperature,
        max_tokens: this.maxOutputTokens,
      })
      .subscribe({
        next: (response) => {
          const text = response.response?.trim() || 'No pude generar respuesta.';
          this.updateBotText(botId, text);
          if ((!this.headerTitle || this.headerTitle === 'Chatbot') && response.course?.nombre) {
            this.headerTitle = response.course.nombre;
          }
          this.isSending = false;
        },
        error: (error) => {
          console.error('Error al hablar con el chatbot del curso', error);
          this.updateBotText(botId, '\n\n[Error] No se pudo completar la respuesta. Intenta nuevamente en unos segundos.');
          this.isSending = false;
        },
      });
  }

  private buildBackendMessages(): CourseChatMessage[] {
    const contents: CourseChatMessage[] = [];
    let seenUser = false;
    for (const m of this.messages) {
      if (m.meta) continue; // never send meta messages
      if (m.from === 'user') seenUser = true;
      if (!seenUser) continue; // skip any bot text before first user
      if (m.from === 'bot' && !m.text) continue;
      contents.push({ role: m.from === 'user' ? 'user' : 'model', content: m.text });
    }
    return contents;
  }

  private updateBotText(id: number, piece: string, append = false) {
    this.messages = this.messages.map((m) =>
      m.id === id ? { ...m, text: append ? (m.text + piece) : piece } : m
    );
  }

  renderMarkdown(md: string): SafeHtml {
    let html = md
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    // code blocks
    html = html.replace(/```[\s\S]*?```/g, (block) => {
      const content = block.replace(/```/g, '').trim();
      return `<pre class="rounded-xl bg-neutral-300 p-3 overflow-auto"><code>${content}</code></pre>`;
    });
    // inline code
    html = html.replace(/`([^`]+)`/g, '<code class="rounded bg-neutral-300 px-1 py-0.5">$1</code>');
    // bold and italic
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // links
    html = html.replace(/\b(https?:\/\/[^\s]+)\b/g, '<a class="text-primary underline" href="$1" target="_blank" rel="noopener">$1</a>');
    // paragraphs
    html = html.split(/\n{2,}/).map(p => `<p class="mb-2">${p}</p>`).join('');
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  private formatChatForExport(): string {
    return this.messages
      .filter((m) => !m.meta)
      .map((m) => `${m.from === 'user' ? 'Usuario' : 'Bot'} (${m.time}): ${m.text}`)
      .join('\n');
  }

  private formatChatStart(date: Date): string {
    const pad = (n: number) => n.toString().padStart(2, '0');
    const day = pad(date.getDate());
    const month = pad(date.getMonth() + 1);
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  private resolveErrorMessage(error: unknown, fallback: string): string {
    if (!error) {
      return fallback;
    }

    if (typeof error === 'string') {
      return error;
    }

    if (error instanceof Error) {
      return error.message || fallback;
    }

    if (typeof error === 'object') {
      const maybe = error as { message?: string; error?: unknown };
      if (typeof maybe?.message === 'string' && maybe.message.trim()) {
        return maybe.message;
      }
      if (maybe?.error) {
        const nested = maybe.error as { msg?: string } | string;
        if (typeof nested === 'string' && nested.trim()) {
          return nested;
        }
        if (typeof nested === 'object' && nested && typeof nested.msg === 'string' && nested.msg.trim()) {
          return nested.msg;
        }
      }
    }

    return fallback;
  }

  private readNavStateValue(state: Record<string, unknown>, key: ChatNavKey): string | undefined {
    const value = state[key];
    return typeof value === 'string' ? value : undefined;
  }

  private readNavStateNumber(state: Record<string, unknown>, key: string): number | null {
    const value = state[key];
    if (typeof value === 'number') {
      return Number.isFinite(value) ? value : null;
    }
    if (typeof value === 'string') {
      const parsed = Number(value);
      return Number.isFinite(parsed) ? parsed : null;
    }
    return null;
  }

}
