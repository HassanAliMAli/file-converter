import apiClient from './api';

interface UploadResponse {
    message: string;
    task_id: string;
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

  // TODO: Add function to check conversion status (using task_id)
  // checkConversionStatus: async (taskId: string): Promise<any> => { ... }

  // TODO: Add function to download converted file
  // downloadFile: async (filePath: string) => { ... }
}; 