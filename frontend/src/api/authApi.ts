import { apiClient } from './client';
import { ApiResponse, User } from '../types';

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authApi = {
  login: async (email: string, password: string) => {
    const res = await apiClient.post<ApiResponse<LoginResponse>>('/auth/login', { email, password });
    return res.data;
  },
  register: async (email: string, password: string, full_name: string, role: string = 'customer') => {
    const res = await apiClient.post<ApiResponse<LoginResponse>>('/auth/register', {
      email,
      password,
      full_name,
      role,
    });
    return res.data;
  },
  getMe: async () => {
    const res = await apiClient.get<ApiResponse<User>>('/auth/me');
    return res.data;
  },
};
