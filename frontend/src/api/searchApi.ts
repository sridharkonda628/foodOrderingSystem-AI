import { apiClient } from './client';
import { ApiResponse, SearchResponseData } from '../types';

export const searchApi = {
  searchNaturalLanguage: async (query: string, limit: number = 8) => {
    const res = await apiClient.post<ApiResponse<SearchResponseData>>('/search', { query, limit });
    return res.data;
  },
};
