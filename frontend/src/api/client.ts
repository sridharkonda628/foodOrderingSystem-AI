import axios from 'axios';

export const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Axios API client configured with:
 * - `withCredentials: true`: Automatically sends and receives secure `HttpOnly` cookies.
 * - Centralized response error handling.
 */
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Enables secure HttpOnly cookie transmission across requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor: handle session expiration (401 Unauthorized)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Return structured error
    return Promise.reject(error);
  }
);
