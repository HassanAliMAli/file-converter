import axios from 'axios';
import { useAuthStore } from '../store'; // Assuming store setup

// Get baseURL from environment variables (set in .env and accessed via Vite)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

if (!import.meta.env.VITE_API_BASE_URL) {
  console.warn("VITE_API_BASE_URL environment variable not set. Defaulting to http://localhost:8000");
}

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Optional: Add response interceptor for handling common errors (e.g., 401 Unauthorized)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token might be invalid or expired
      console.error('Unauthorized request - logging out.');
      useAuthStore.getState().logout();
      // Optionally redirect to login page
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient; 