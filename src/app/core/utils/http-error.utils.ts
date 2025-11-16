import { HttpErrorResponse } from '@angular/common/http';

type ErrorRecord = Record<string, unknown>;

export function extractErrorMessage(error: unknown): string | null {
  if (!error) {
    return null;
  }

  const httpError = error as Partial<HttpErrorResponse>;
  const backendMessage = getBackendMessage(httpError.error);
  const raw = backendMessage ?? httpError.message ?? httpError.statusText ?? httpError.error;

  return formatRawMessage(raw);
}

export function normalizeErrorString(message: string): string {
  const trimmed = message.trim();
  if (!trimmed.startsWith('{') || !trimmed.endsWith('}')) {
    return trimmed;
  }

  try {
    const parsed = JSON.parse(
      trimmed
        .replace(/'/g, '"')
        .replace(/None/g, 'null')
        .replace(/True/g, 'true')
        .replace(/False/g, 'false'),
    );

    if (typeof parsed === 'string') {
      return parsed;
    }

    if (Array.isArray(parsed) || isRecord(parsed)) {
      return formatRawMessage(parsed) ?? trimmed;
    }

    return trimmed;
  } catch {
    return trimmed;
  }
}

function getBackendMessage(payload: unknown): unknown {
  if (isRecord(payload) && 'msg' in payload) {
    return payload['msg'];
  }
  return null;
}

function formatRawMessage(raw: unknown): string | null {
  if (!raw) {
    return null;
  }

  if (typeof raw === 'string') {
    return normalizeErrorString(raw);
  }

  if (Array.isArray(raw)) {
    return raw.map(stringifyItem).join(' ');
  }

  if (isRecord(raw)) {
    const parts: unknown[] = [];
    Object.values(raw).forEach((value) => {
      if (Array.isArray(value)) {
        parts.push(...value);
      } else {
        parts.push(value);
      }
    });
    return parts.map(stringifyItem).join(' ');
  }

  return null;
}

function stringifyItem(item: unknown): string {
  return typeof item === 'string' ? item : JSON.stringify(item);
}

function isRecord(value: unknown): value is ErrorRecord {
  return typeof value === 'object' && value !== null;
}
