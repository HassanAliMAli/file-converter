import { Routes, Route, Link } from 'react-router-dom'
import React, { useEffect, useState } from 'react';
// Placeholder Pages (will be moved to /pages directory later)
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import NotFoundPage from './pages/NotFoundPage';
import ProtectedRoute from './components/ProtectedRoute';
import { useAuthStore } from './store';
import { authService } from './services/authService';

// Placeholder Layout (can be expanded later)
function Layout() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <nav className="bg-blue-600 dark:bg-blue-800 p-4 text-white shadow-md">
        <ul className="flex space-x-4 justify-center">
          <li><Link to="/" className="hover:underline">Home</Link></li>
          <li><Link to="/login" className="hover:underline">Login</Link></li>
          <li><Link to="/register" className="hover:underline">Register</Link></li>
          <li><Link to="/dashboard" className="hover:underline">Dashboard</Link></li>
        </ul>
      </nav>
      <main className="flex-grow container mx-auto p-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          {/* Add other routes here */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
      <footer className="bg-gray-200 dark:bg-gray-800 p-4 text-center text-sm text-gray-600 dark:text-gray-400">
        © {new Date().getFullYear()} Universal File Converter. All rights reserved.
      </footer>
    </div>
  );
}

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const token = useAuthStore((state) => state.token);

  useEffect(() => {
    const initializeAuth = async () => {
      if (token) {
        try {
          console.log("Attempting to fetch current user...");
          await authService.fetchCurrentUser();
          console.log("Fetched current user successfully.");
        } catch {
          console.warn("Token found, but failed to fetch user. Logging out.");
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, [token]);

  if (isLoading) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>;
  }

  return <Layout />;
}

export default App;
