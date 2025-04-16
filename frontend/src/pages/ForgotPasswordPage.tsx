import React from 'react';

const ForgotPasswordPage: React.FC = () => {
  // TODO: Implement forgot password form (email input)
  return (
    <div className="max-w-md mx-auto mt-10 p-8 bg-white dark:bg-gray-800 shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">Forgot Password</h2>
      <p className="text-center text-red-500">Forgot Password Form Placeholder</p>
      {/* Form to submit email -> calls /auth/forgot-password */}
    </div>
  );
};

export default ForgotPasswordPage; 