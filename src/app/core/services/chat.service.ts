import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_BASE_URL } from '../tokens/api.token';

export interface CourseChatMessage {
  role: 'user' | 'model';
  content: string;
}

export interface CourseChatRequest {
  messages: CourseChatMessage[];
  temperature?: number;
  max_tokens?: number;
}

export interface CourseChatResponse {
  response: string;
  model: string;
  course: {
    id: number;
    nombre: string;
  };
}

interface CourseChatErrorResponse {
  msg?: string;
}

@Injectable({ providedIn: 'root' })
export class ChatService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  sendCourseMessage(courseId: number, body: CourseChatRequest): Observable<CourseChatResponse> {
    return this.http
      .post<CourseChatResponse | CourseChatErrorResponse>(
        `${this.apiBaseUrl}/courses/${courseId}/chat`,
        body,
      )
      .pipe(
        map((payload) => {
          if ('response' in payload && typeof payload.response === 'string') {
            return payload;
          }
          let message = 'No se pudo procesar la respuesta del chatbot.';
          if ('msg' in payload && typeof payload.msg === 'string' && payload.msg.trim()) {
            message = payload.msg;
          }
          throw new Error(message);
        }),
      );
  }
}
