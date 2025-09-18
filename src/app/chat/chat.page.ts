import { Component, inject } from '@angular/core';
import {
  IonButton,
  IonContent,
  IonFooter,
  IonIcon,
  IonInput,
  IonItem,
  IonToolbar,
} from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { addIcons } from 'ionicons';
import { send, trashOutline } from 'ionicons/icons';
import { TopbarComponent } from '../components/topbar/topbar.component';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

interface ChatMessage {
  id: number;
  from: 'user' | 'bot';
  text: string;
  time: string;
  meta?: boolean; // not sent to LLM
}

@Component({
  selector: 'app-chat',
  templateUrl: 'chat.page.html',
  imports: [
    CommonModule,
    FormsModule,
    TopbarComponent,
    IonButton,
    IonContent,
    IonFooter,
    IonIcon,
    IonInput,
    IonItem,
    IonToolbar,
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

  constructor() {
    addIcons({ send, trashOutline });
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

  private buildContents() {
    const contents: any[] = [];
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

  private buildRequestBody(opts?: { omitSystemInstruction?: boolean; prependPromptAsUser?: boolean }) {
    const body: any = {
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
      let body: any = this.buildRequestBody();
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
          const json: any = await retry.json();
          const text: string = json?.candidates?.[0]?.content?.parts?.map((p: any) => p.text).join('') || 'No pude generar respuesta.';
          this.updateBotText(botId, text);
          return;
        }
        throw new Error(`HTTP ${resp.status}`);
      }
      const json: any = await resp.json();
      const text: string = json?.candidates?.[0]?.content?.parts?.map((p: any) => p.text).join('') || 'No pude generar respuesta.';
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
}
