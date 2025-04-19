// Define a type for expected Axios error structure with detail
// This helps in safely accessing nested properties
export interface AxiosErrorDetail {
  response?: {
    data?: {
      detail?: string | { msg: string }[]; // Can be string or array (like FastAPI validation)
    };
  };
  message?: string; // Standard error message property
} 