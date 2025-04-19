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

      // Set token in store immediately so fetchCurrentUser can use it
      useAuthStore.getState().setToken(access_token); 

      // Fetch user details using the existing function
      const user = await authService.fetchCurrentUser(); 

      if (user) {
        // The fetchCurrentUser function already updated the store, 
        // but we log success here after confirming user was fetched.
        console.log("Login and user fetch successful");
      } else {
        // This case might happen if /users/me fails immediately after login
        // fetchCurrentUser already handles logout in case of error
        console.error("Login succeeded but fetching user failed. User has been logged out.");
        // Throw an error to indicate the overall login process failed
        throw new Error("Login succeeded but could not retrieve user details.");
      }

    } catch (error) {
      console.error('Login failed:', error);
      // Ensure logout if any part of the process failed
      useAuthStore.getState().logout();
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
    // Add check: No need to fetch if no token exists
    const token = useAuthStore.getState().token;
    if (!token) {
      console.log("No token found, cannot fetch current user.");
      // Ensure user is logged out if somehow the state is inconsistent
      useAuthStore.getState().logout(); 
      return null;
    }
    
    try {
        const response = await apiClient.get<User>('/users/me');
        const user = response.data;
        // Update store with fetched user data AND the token we already have
        useAuthStore.getState().setUserAndToken(user, token);
        return user;
    } catch (error) {
        console.error("Failed to fetch current user:", error);
        // If fetching fails (e.g., invalid token), ensure logout
        useAuthStore.getState().logout();
        return null;
    }
  },

  resetPassword: async (token: string, newPassword: string): Promise<void> => {
    try {
      // The endpoint likely expects a payload like { token, password }
      await apiClient.post('/auth/reset-password', { 
          token: token, 
          password: newPassword 
      });
      console.log("Password reset successful for token:", token);
    } catch (error) {
      console.error("Password reset failed:", error);
      // Re-throw the error for the component to handle and display
      throw error; 
    }
  },

}; 