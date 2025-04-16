import React, { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/authService';

interface RegisterFormInputs {
  email: string;
  password: string;
  confirmPassword: string;
}

const RegisterPage: React.FC = () => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormInputs>();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState<string | null>(null);

  // Watch password field to validate confirmPassword
  const password = watch('password');

  const onSubmit: SubmitHandler<RegisterFormInputs> = async (data) => {
    setServerError(null);
    try {
      await authService.register({ email: data.email, password: data.password });
      // Optional: Log the user in automatically after registration
      // await authService.login({ username: data.email, password: data.password });
      // navigate('/dashboard');

      // Redirect to login page after successful registration
      alert('Registration successful! Please log in.'); // Simple feedback
      navigate('/login');
    } catch (error: unknown) { // Use unknown for safer error handling
      console.error('Registration failed:', error);
      let errorMsg = "Registration failed. Please try again.";
       if (typeof error === 'object' && error !== null && 'response' in error) {
        const axiosError = error as { response?: { data?: { detail?: string | { msg: string }[] } } };
        // Handle potential array of errors from FastAPI validation
        if (axiosError.response?.data?.detail && Array.isArray(axiosError.response.data.detail)) {
             errorMsg = axiosError.response.data.detail.map(d => d.msg).join(', ');
        } else if (axiosError.response?.data?.detail && typeof axiosError.response.data.detail === 'string') {
            errorMsg = axiosError.response.data.detail;
        } else if (axiosError.response?.data?.detail) {
             errorMsg = JSON.stringify(axiosError.response.data.detail);
        }
      }
      setServerError(errorMsg);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-8 bg-white dark:bg-gray-800 shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">Register</h2>
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
            {...register("email", {
              required: "Email is required",
              pattern: { value: /\S+@\S+\.\S+/, message: "Invalid email address" },
            })}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
            aria-invalid={errors.email ? "true" : "false"}
          />
          {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email.message}</p>}
        </div>

        <div className="mb-4">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
          <input
            id="password"
            type="password"
            {...register("password", {
              required: "Password is required",
              minLength: { value: 8, message: "Password must be at least 8 characters" },
            })}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
            aria-invalid={errors.password ? "true" : "false"}
          />
          {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>}
        </div>

        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Confirm Password</label>
          <input
            id="confirmPassword"
            type="password"
            {...register("confirmPassword", {
              required: "Please confirm your password",
              validate: (value) =>
                value === password || "Passwords do not match",
            })}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.confirmPassword ? 'border-red-500' : 'border-gray-300'}`}
            aria-invalid={errors.confirmPassword ? "true" : "false"}
          />
          {errors.confirmPassword && <p className="mt-1 text-xs text-red-600">{errors.confirmPassword.message}</p>}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ease-in-out disabled:opacity-50"
        >
          {isSubmitting ? 'Registering...' : 'Register'}
        </button>
      </form>
        <p className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
        Already have an account? {' '}
        <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500 hover:underline">
          Login here
        </Link>
      </p>
    </div>
  );
};

export default RegisterPage; 