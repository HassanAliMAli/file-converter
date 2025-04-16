import React from 'react';
import { useParams } from 'react-router-dom';

const ResetPasswordPage: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  // TODO: Implement reset password form (new password, confirm password)
  return (
    <div className="max-w-md mx-auto mt-10 p-8 bg-white dark:bg-gray-800 shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">Reset Password</h2>
      <p>Token: {token}</p>
      <p className="text-center text-red-500">Reset Password Form Placeholder</p>
      {/* Form to submit token, new password -> calls /auth/reset-password */}
    </div>
  );
};

export default ResetPasswordPage; 