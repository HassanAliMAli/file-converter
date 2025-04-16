import apiClient from './api';
import { useAuthStore } from '../store';

// Define types for request/response based on backend schemas (adjust as needed)
interface LoginCredentials {
  username: string; // fastapi-users uses email as username by default
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  // Add other required fields (e.g., is_active, is_superuser defaults?)
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

// UserRead schema from backend (adjust based on actual schema)
interface User {
    id: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
}

export const authService = {
  login: async (credentials: LoginCredentials): Promise<void> => {
    // fastapi-users /login endpoint expects form data
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    try {
      const response = await apiClient.post<TokenResponse>('/auth/jwt/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      const { access_token } = response.data;

      // TODO: Fetch user details after successful login (/users/me)
      // For now, we simulate user data based on email
      const simulatedUser = { id: 'unknown', email: credentials.username }; // Replace with actual user fetch
      useAuthStore.getState().login(simulatedUser, access_token);
      console.log("Login successful");
    } catch (error) {
      console.error('Login failed:', error);
      // Re-throw or handle error display
      throw error;
    }
  },

  register: async (data: RegisterData): Promise<User> => {
    try {
      const response = await apiClient.post<User>('/auth/register', data);
      console.log("Registration successful:", response.data);
      // Optionally log the user in immediately after registration
      // await authService.login({ username: data.email, password: data.password });
      return response.data;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  },

  logout: (): void => {
    useAuthStore.getState().logout();
    console.log("Logged out");
  },

  fetchCurrentUser: async (): Promise<User | null> => {
    try {
        const response = await apiClient.get<User>('/users/me');
        // Update store with fetched user data
        const user = response.data;
        const token = useAuthStore.getState().token; // Get existing token
        if (token) {
             useAuthStore.getState().login(user, token);
        }
        return user;
    } catch (error) {
        console.error("Failed to fetch current user:", error);
        // If fetching fails (e.g., invalid token), ensure logout
        useAuthStore.getState().logout();
        return null;
    }
  },

}; 