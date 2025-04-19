import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware'; // Use persist middleware

// Define the User interface based on authService.ts
interface User {
    id: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null; 
  token: string | null;
  // Renamed login action to setUserAndToken for clarity
  setUserAndToken: (userData: User, token: string) => void; 
  setToken: (token: string) => void; // Action to only set the token
  logout: () => void;
}

// Use persist middleware to automatically save/load token to localStorage
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      user: null,
      token: null, // Initial state is null, persist middleware loads it

      // Action to set both user and token (typically after /users/me succeeds)
      setUserAndToken: (userData, token) => {
        set({ isAuthenticated: true, user: userData, token: token });
      },

      // Action to set only the token (typically right after /auth/jwt/login succeeds)
      setToken: (token) => {
        // Set token but keep isAuthenticated false until user is fetched
        set({ token: token, isAuthenticated: false, user: null });
      },

      logout: () => {
        // Middleware handles removing the token from storage
        set({ isAuthenticated: false, user: null, token: null });
      },
    }),
    {
      name: 'auth-storage', // Name of the item in storage
      storage: createJSONStorage(() => localStorage), // Use localStorage
      partialize: (state) => ({ token: state.token }), // Only persist the token
    }
  )
);

// Initialize auth state on app load
// This replaces the previous TODO block
const initializeAuthState = async () => {
  const token = useAuthStore.getState().token;
  if (token) {
    console.log("Found token in storage, attempting to fetch user...");
    try {
        // Dynamically import authService to avoid circular dependencies at module load time
        const { authService } = await import('../services/authService'); 
        await authService.fetchCurrentUser();
        console.log("User fetch successful on initial load.");
    } catch (error) {
        console.error("Failed to fetch user on initial load:", error);
        // fetchCurrentUser should handle logout on error, but ensure state is clean
        useAuthStore.getState().logout(); 
    }
  } else {
    console.log("No auth token found in storage.");
  }
};

// Call initialization logic once the store is created
initializeAuthState(); 