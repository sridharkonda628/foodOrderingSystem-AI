import axios from 'axios';

export const API_BASE_URL = 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach JWT token if present
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('kpitech_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't auto redirect on login page
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('kpitech_token');
        localStorage.removeItem('kpitech_user');
      }
    }
    return Promise.reject(error);
  }
);
