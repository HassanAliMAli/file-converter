import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/authService';
// import { useAuthStore } from '../store'; // Login action is called within authService

interface LoginFormInputs {
  email: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormInputs>();
  const navigate = useNavigate();
  // const login = useAuthStore((state) => state.login); // Login action is called within authService
  const [serverError, setServerError] = useState<string | null>(null);

  const onSubmit: SubmitHandler<LoginFormInputs> = async (data) => {
    setServerError(null); // Clear previous errors
    try {
      // Use username = email for fastapi-users
      await authService.login({ username: data.email, password: data.password });
      // Login function in authService now handles setting store state
      // await authService.fetchCurrentUser(); // Fetch user after login is better
      navigate('/dashboard'); // Redirect to dashboard on successful login
    } catch (error: unknown) { // Use unknown for safer error handling
      console.error('Login failed:', error);
      let errorMsg = "Login failed. Please check your credentials.";
      if (typeof error === 'object' && error !== null && 'response' in error) {
        const axiosError = error as { response?: { data?: { detail?: string } } };
        errorMsg = axiosError.response?.data?.detail || errorMsg;
      }
      setServerError(errorMsg);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-8 bg-white dark:bg-gray-800 shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">Login</h2>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        {serverError && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {serverError}
          </div>
        )}
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
          <input
            id="email"
            type="email"
            {...register("email", { required: "Email is required", pattern: { value: /\S+@\S+\.\S+/, message: "Invalid email address" } })}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
            aria-invalid={errors.email ? "true" : "false"}
          />
          {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email.message}</p>}
        </div>

        <div className="mb-6">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
          <input
            id="password"
            type="password"
            {...register("password", { required: "Password is required" })}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
            aria-invalid={errors.password ? "true" : "false"}
          />
          {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ease-in-out disabled:opacity-50"
        >
          {isSubmitting ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
        Don't have an account? {' '}
        <Link to="/register" className="font-medium text-blue-600 hover:text-blue-500 hover:underline">
          Register here
        </Link>
      </p>
    </div>
  );
};

export default LoginPage; 