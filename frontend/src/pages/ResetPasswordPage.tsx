import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import ErrorMessage from '../components/ErrorMessage';
import { AxiosErrorDetail } from '../types/errors';
import { authService } from '../services/authService';

// Zod schema for validation
const passwordSchema = z.object({
  password: z.string().min(8, 'Password must be at least 8 characters long'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"], // path of error
});

type PasswordFormInputs = z.infer<typeof passwordSchema>;

// Utility function to parse errors (kept inline since file creation failed earlier)
const parseApiError = (
    error: unknown,
    defaultMessage = "An unexpected error occurred. Please try again."
): string => {
    if (typeof error === 'object' && error !== null) {
        const axiosError = error as AxiosErrorDetail; // Use type assertion
        if (axiosError.response?.data?.detail) {
            const detail = axiosError.response.data.detail;
            if (typeof detail === 'string') { return detail; }
            if (Array.isArray(detail) && detail.length > 0 && typeof detail[0]?.msg === 'string') {
                return detail.map(d => d.msg).join(', ');
            }
            if (typeof detail === 'object') { try { return JSON.stringify(detail); } catch (_) {} }
        }
        if (axiosError.message) { return axiosError.message; }
    }
    return defaultMessage;
};

const ResetPasswordPage: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset, // Add reset function from useForm
  } = useForm<PasswordFormInputs>({
    resolver: zodResolver(passwordSchema),
  });
  const [serverError, setServerError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const onSubmit: SubmitHandler<PasswordFormInputs> = async (data) => {
    setServerError(null);
    setSuccessMessage(null);

    if (!token) {
        setServerError("Password reset token is missing from the URL.");
        return;
    }

    try {
      console.log("Submitting new password with token:", token, "Data:", data.password);
      await authService.resetPassword(token, data.password);

      setSuccessMessage("Password has been reset successfully! You can now log in.");
      reset(); // Clear form
      setTimeout(() => navigate('/login'), 3000);

    } catch (error: unknown) {
      console.error('Password reset failed:', error);
      const errorMsg = parseApiError(error, "Password reset failed. The link may be invalid or expired.");
      setServerError(errorMsg);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-8 bg-white dark:bg-gray-800 shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">Reset Your Password</h2>

      {successMessage && (
        <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
          {successMessage}
        </div>
      )}

      <ErrorMessage message={serverError} />

      {!successMessage && (
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="mb-4">
            <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">New Password</label>
            <input
              type="password"
              id="password"
              {...register("password")}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
              aria-invalid={errors.password ? "true" : "false"}
              required
            />
            {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>}
          </div>

          <div className="mb-6">
            <label htmlFor="confirmPassword" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">Confirm New Password</label>
            <input
              type="password"
              id="confirmPassword"
              {...register("confirmPassword")}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white ${errors.confirmPassword ? 'border-red-500' : 'border-gray-300'}`}
              aria-invalid={errors.confirmPassword ? "true" : "false"}
              required
            />
            {errors.confirmPassword && <p className="mt-1 text-xs text-red-600">{errors.confirmPassword.message}</p>}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50"
          >
            {isSubmitting ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>
      )}
    </div>
  );
};

export default ResetPasswordPage; 