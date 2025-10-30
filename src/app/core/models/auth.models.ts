export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  rut: string;
  email: string;
  region: string;
  comuna: string;
  password: string;
  institution_id: number;
  grade_id?: number | null;
  role?: 'student' | 'teacher' | 'admin';
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface AuthInstitution {
  id: number;
  nombre: string;
  direccion?: string | null;
  paginaweb?: string | null;
  colorinstitucional?: string | null;
  logotipo?: string | null;
  fundacion?: string | null;
  courses_count?: number;
}

export interface AuthGrade {
  id: number;
  name: string;
  order: number;
}

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
  rut: string;
  region: string;
  comuna: string;
  institution_id: number | null;
  grade_id: number | null;
  institution?: AuthInstitution | null;
  grade?: AuthGrade | null;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: AuthUser;
}

export interface RegisterResponse {
  msg: string;
  user: AuthUser;
}

export interface StoredSession {
  tokens: AuthTokens;
  user: AuthUser;
}
