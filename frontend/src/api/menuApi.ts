import { apiClient } from './client';
import { ApiResponse, Category, MenuItem } from '../types';

export const menuApi = {
  getCategories: async () => {
    const res = await apiClient.get<ApiResponse<Category[]>>('/menu/categories');
    return res.data;
  },
  getMenuItems: async (params?: {
    category_id?: number;
    is_vegetarian?: boolean;
    is_spicy?: boolean;
    available_only?: boolean;
  }) => {
    const res = await apiClient.get<ApiResponse<MenuItem[]>>('/menu', { params });
    return res.data;
  },
  getMenuItem: async (id: string) => {
    const res = await apiClient.get<ApiResponse<MenuItem>>(`/menu/${id}`);
    return res.data;
  },
  createMenuItem: async (data: Partial<MenuItem>) => {
    const res = await apiClient.post<ApiResponse<MenuItem>>('/menu', data);
    return res.data;
  },
  updateMenuItem: async (id: string, data: Partial<MenuItem>) => {
    const res = await apiClient.put<ApiResponse<MenuItem>>(`/menu/${id}`, data);
    return res.data;
  },
  toggleAvailability: async (id: string, is_available: boolean) => {
    const res = await apiClient.patch<ApiResponse<MenuItem>>(`/menu/${id}/availability`, { is_available });
    return res.data;
  },
  deleteMenuItem: async (id: string) => {
    const res = await apiClient.delete<ApiResponse<{ id: string }>>(`/menu/${id}`);
    return res.data;
  },
};
