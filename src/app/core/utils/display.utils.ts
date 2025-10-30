const baseCache = new Map<string, string>();

export function buildInitials(value: string | null | undefined, fallback = 'UX'): string {
  const word = (value ?? '').trim();
  if (!word) {
    return fallback;
  }
  const parts = word.split(/\s+/).filter(Boolean);
  const first = parts[0]?.[0] ?? '';
  const second = parts[1]?.[0] ?? parts[0]?.[1] ?? '';
  const initials = `${first}${second}`.toUpperCase();
  return initials || word.slice(0, 2).toUpperCase();
}

export function resolveUploadedAssetUrl(apiBaseUrl: string, relativePath: string | null | undefined): string | null {
  if (!relativePath) {
    return null;
  }
  if (/^https?:\/\//i.test(relativePath)) {
    return relativePath;
  }

  const base = computeAssetsBaseUrl(apiBaseUrl);
  const cleaned = relativePath.replace(/\\/g, '/');
  const normalized = cleaned.startsWith('/')
    ? cleaned
    : cleaned.startsWith('uploads')
    ? `/${cleaned}`
    : `/uploads/${cleaned}`;

  return `${base}${normalized}`;
}

function computeAssetsBaseUrl(apiBaseUrl: string): string {
  const cached = baseCache.get(apiBaseUrl);
  if (cached) {
    return cached;
  }

  let computed = apiBaseUrl;
  try {
    const url = new URL(apiBaseUrl);
    const trimmedPath = url.pathname.replace(/\/api\/?$/i, '/');
    url.pathname = trimmedPath;
    url.search = '';
    url.hash = '';
    computed = url.toString();
  } catch {
    computed = apiBaseUrl.replace(/\/api\/?$/i, '/');
  }

  if (computed.endsWith('/')) {
    computed = computed.slice(0, -1);
  }
  baseCache.set(apiBaseUrl, computed);
  return computed;
}

export function buildCourseBadge(name: string | null | undefined): string {
  const trimmed = (name ?? '').trim();
  if (!trimmed) {
    return '📘';
  }
  const initials = trimmed
    .split(/\s+/)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .filter(Boolean)
    .slice(0, 2)
    .join('');
  return initials || trimmed[0]!.toUpperCase();
}
