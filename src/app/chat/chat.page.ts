import { Component, inject } from '@angular/core';
import { IonButton, IonContent, IonFooter, IonIcon, IonInput } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { addIcons } from 'ionicons';
import { send, trashOutline, ellipsisHorizontal, chevronBack, downloadOutline, copyOutline } from 'ionicons/icons';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { NavController } from '@ionic/angular';
import { ScreenHeaderComponent } from '../components/screen-header/screen-header.component';
import { ActionMenuComponent, ActionMenuItem } from '../components/action-menu/action-menu.component';

interface ChatMessage {
  id: number;
  from: 'user' | 'bot';
  text: string;
  time: string;
  meta?: boolean; // not sent to LLM
}

type ChatNavKey = 'title' | 'subtitle' | 'color' | 'emoji';

interface GenerativePart {
  text?: string;
}

interface GenerativeContent {
  role: 'user' | 'model';
  parts: GenerativePart[];
}

interface GenerationConfig {
  temperature: number;
  maxOutputTokens: number;
}

interface GenerateContentRequest {
  contents: GenerativeContent[];
  generationConfig: GenerationConfig;
  systemInstruction?: { parts: GenerativePart[] };
}

interface GenerateContentResponse {
  candidates?: {
    content?: {
      parts?: GenerativePart[];
    };
  }[];
}

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
  ],
})
export class ChatPage {

  API_KEY = ''; /* Aqui va la apiKey de OpenAI */
  MODEL = 'models/gemma-3-1b-it';

  messages: ChatMessage[] = [
    { id: 1, from: 'bot', text: 'Nueva conversación iniciada. ¿En qué te ayudo?', time: this.now(), meta: true },
  ];

  draft = '';
  isSending = false;
  systemPrompt = 'Eres un asistente útil y conciso que responde en español con un tono institucional cercano.';
  temperature = 0.6;
  maxOutputTokens = 2048;
  private readonly sanitizer = inject(DomSanitizer);
  private readonly router = inject(Router);
  private readonly nav = inject(NavController);

  // Header props (populated from navigation state)
  headerTitle = 'Chatbot';
  headerSubtitle?: string;
  headerColor = 'var(--color-primary)';
  headerEmoji = '🤖';
  isOptionsOpen = false;
  optionsEvent?: Event;
  chatStartedAt = new Date();
  chatStartedDisplay = this.formatChatStart(this.chatStartedAt);

  readonly menuActions: ActionMenuItem[] = [
    { id: 'download', label: 'Descargar conversación', icon: 'download-outline' },
    { id: 'copy', label: 'Copiar conversación', icon: 'copy-outline' },
  ];

  constructor() {
    addIcons({ send, trashOutline, ellipsisHorizontal, chevronBack, downloadOutline, copyOutline });

    const navState = this.router.getCurrentNavigation()?.extras?.state as Record<string, unknown> | undefined;
    if (navState) {
      this.headerTitle = this.readNavStateValue(navState, 'title') ?? this.headerTitle;
      this.headerSubtitle = this.readNavStateValue(navState, 'subtitle') ?? this.headerSubtitle;
      this.headerColor = this.readNavStateValue(navState, 'color') ?? this.headerColor;
      this.headerEmoji = this.readNavStateValue(navState, 'emoji') ?? this.headerEmoji;
    }
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
    this.generateNonStream(botId);
  }

  clearChat() {
    this.messages = [
      { id: Date.now(), from: 'bot', text: 'Nueva conversación iniciada. ¿En qué te ayudo?', time: this.now() },
    ];
  }

  private now() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  private buildContents(): GenerativeContent[] {
    const contents: GenerativeContent[] = [];
    let seenUser = false;
    for (const m of this.messages) {
      if (m.meta) continue; // never send meta messages
      if (m.from === 'user') seenUser = true;
      if (!seenUser) continue; // skip any bot text before first user
      if (m.from === 'bot' && !m.text) continue;
      contents.push({ role: m.from === 'user' ? 'user' : 'model', parts: [{ text: m.text }] });
    }
    return contents;
  }

  private buildRequestBody(opts?: { omitSystemInstruction?: boolean; prependPromptAsUser?: boolean }): GenerateContentRequest {
    const body: GenerateContentRequest = {
      contents: this.buildContents(),
      generationConfig: {
        temperature: this.temperature,
        maxOutputTokens: this.maxOutputTokens,
      },
    };
    const prompt = this.systemPrompt?.trim();
    if (prompt && !opts?.omitSystemInstruction) {
      body.systemInstruction = { parts: [{ text: prompt }] };
    } else if (prompt && opts?.prependPromptAsUser) {
      body.contents = [
        { role: 'user', parts: [{ text: `INSTRUCCIONES: ${prompt}` }] },
        ...body.contents,
      ];
    }
    return body;
  }

  private async generateNonStream(botId: number) {
    try {
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.modelId}:generateContent?key=${this.API_KEY}`;
      let body = this.buildRequestBody();
      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!resp.ok) {
        const errText = await resp.text().catch(() => '');
        console.error('Non-stream HTTP error', resp.status, errText);
        if (errText.includes('Developer instruction is not enabled')) {
          body = this.buildRequestBody({ omitSystemInstruction: true, prependPromptAsUser: true });
          const retry = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
          });
          if (!retry.ok) throw new Error(`HTTP ${retry.status}`);
          const json = (await retry.json()) as GenerateContentResponse;
          const text = this.extractResponseText(json) ?? 'No pude generar respuesta.';
          this.updateBotText(botId, text);
          return;
        }
        throw new Error(`HTTP ${resp.status}`);
      }
      const json = (await resp.json()) as GenerateContentResponse;
      const text = this.extractResponseText(json) ?? 'No pude generar respuesta.';
      this.updateBotText(botId, text);
    } catch (e) {
      console.error('Fallback no-stream también falló:', e);
      this.updateBotText(botId, '\n\n[Error] No se pudo completar la respuesta. Verifica API key/modelo o CORS.');
    }
  }

  private get modelId(): string {
    return (this.MODEL || '').replace(/^models\//, '');
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

  private readNavStateValue(state: Record<string, unknown>, key: ChatNavKey): string | undefined {
    const value = state[key];
    return typeof value === 'string' ? value : undefined;
  }

  private extractResponseText(response: GenerateContentResponse): string | undefined {
    const candidates = response.candidates ?? [];
    for (const candidate of candidates) {
      const parts = candidate.content?.parts ?? [];
      const combined = parts.map((part) => part.text ?? '').join('');
      if (combined.trim()) {
        return combined;
      }
    }
    return undefined;
  }
}
