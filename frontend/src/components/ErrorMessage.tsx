import React from 'react';

interface ErrorMessageProps {
  message: string | null | undefined;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  if (!message) {
    return null; // Don't render anything if there's no message
  }

  return (
    <div 
      className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"
      role="alert"
    >
      {message}
    </div>
  );
};

export default ErrorMessage; 