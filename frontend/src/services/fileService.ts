import apiClient from './api';

interface UploadResponse {
    message: string;
    task_id: string;
    // Add conversion_id if backend sends it
    conversion_id?: string; 
}

// Interface matching the data returned by GET /convert/status/{conversion_id}
interface ConversionStatusResponse {
    conversion_id: string;
    task_id: string | null;
    status: string; // PENDING, PROCESSING, COMPLETED, FAILED
    output_format: string;
    converted_file_path: string | null;
    error_message: string | null;
    created_at: string; // ISO date string
    updated_at: string; // ISO date string
    original_filename: string;
}

export const fileService = {
  uploadFile: async (file: File, outputFormat: string): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('output_format', outputFormat);

    try {
      // Use apiClient but override Content-Type for FormData
      const response = await apiClient.post<UploadResponse>('/convert/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        // Optional: Add progress tracking
        // onUploadProgress: (progressEvent) => {
        //   const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        //   console.log(`Upload Progress: ${percentCompleted}%`);
        // },
      });
      return response.data;
    } catch (error) {
      console.error('File upload failed:', error);
      throw error; // Re-throw for component to handle
    }
  },

  // Define the expected shape of the status response from the backend
  // Based on the backend endpoint: /convert/status/{conversion_id}
  checkConversionStatus: async (conversionId: string): Promise<ConversionStatusResponse> => {
    try {
      const response = await apiClient.get<ConversionStatusResponse>(`/convert/status/${conversionId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching status for conversion ${conversionId}:`, error);
      throw error;
    }
  },

  // Function to initiate the download of the converted file
  // This doesn't download the file directly but provides the URL or triggers the download
  getDownloadUrl: (conversionId: string): string => {
    // Corresponds to GET /convert/download/{conversion_id} in backend
    // We return the URL that the browser should navigate to or use in an <a> tag
    // The actual file download is handled by the browser hitting the backend endpoint
    const baseUrl = apiClient.defaults.baseURL;

    // Base URL is always set (env var or default) in api.ts, this check is likely not needed
    // if (!baseUrl) {
    //     console.error("API base URL is not configured in apiClient.");
    //     // Return a non-functional path or throw an error
    //     return "#";
    // }
    
    // If baseUrl is somehow undefined despite the setup in api.ts, log a warning
    if (!baseUrl) {
      console.warn("apiClient.defaults.baseURL is unexpectedly undefined or empty. Check api.ts and environment variables.");
      // Return a non-functional URL or handle appropriately
      return `#error-base-url-missing`; 
    }
    
    // Ensure no trailing slash in baseUrl and no leading slash in the path part
    const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
    const path = `/convert/download/${conversionId}`; 
    
    return `${cleanBaseUrl}${path}`;
  },

  // Optional: Add other file-related service calls here
}; 