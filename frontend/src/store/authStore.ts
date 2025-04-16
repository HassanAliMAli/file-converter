import { create } from 'zustand';

interface AuthState {
  isAuthenticated: boolean;
  user: { id: string; email: string } | null; // Define a basic user structure
  token: string | null;
  login: (userData: { id: string; email: string }, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  user: null,
  token: localStorage.getItem('authToken') || null, // Attempt to load token from storage

  login: (userData, token) => {
    localStorage.setItem('authToken', token);
    set({ isAuthenticated: true, user: userData, token: token });
  },

  logout: () => {
    localStorage.removeItem('authToken');
    set({ isAuthenticated: false, user: null, token: null });
  },
}));

// Initialize auth state based on token existence (optional but good practice)
const initialToken = localStorage.getItem('authToken');
if (initialToken) {
  // TODO: In a real app, you would verify the token and fetch user data here
  // For now, we assume token presence means logged in (potentially insecure)
  // useAuthStore.setState({ isAuthenticated: true, token: initialToken });
  // A better approach involves an initial API call to /users/me
} 