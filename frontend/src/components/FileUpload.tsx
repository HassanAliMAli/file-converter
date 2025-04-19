import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { fileService } from '../services/fileService';

// TODO: Define supported output formats dynamically (e.g., from config or API)
const supportedOutputFormats = ['pdf', 'png', 'jpg', 'txt'];

interface FileUploadProps {
  // Define a more specific type for the success response if possible (matching backend)
  onUploadSuccess?: (response: { message: string; task_id: string; conversion_id?: string }) => void;
  // Define a more specific type for the error if using AxiosError etc.
  onUploadError?: (error: Error) => void;
}

export function FileUpload({ onUploadSuccess, onUploadError }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedFormat, setSelectedFormat] = useState<string>(supportedOutputFormats[0]);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
      setError(null); // Clear previous errors
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    // TODO: Consider adding client-side validation for file type/size
    // accept: { 'image/png': ['.png'], 'image/jpeg': ['.jpg', '.jpeg'], ... }
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }
    if (!selectedFormat) {
      setError('Please select an output format.');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      // TODO: Implement actual progress tracking if needed using Axios onUploadProgress
      const response = await fileService.uploadFile(selectedFile, selectedFormat);
      console.log('Upload successful:', response);
      setIsUploading(false);
      setSelectedFile(null); // Clear selection after upload
      if (onUploadSuccess) {
        // Assuming backend returns conversion_id in the response now
        // Adjust based on actual backend response structure if different
        onUploadSuccess(response); // Use the inferred type
      }
    } catch (err) { // Catch specific error types if possible, e.g., AxiosError
      console.error('Upload failed:', err);
      // Try to extract backend error detail, fallback to standard error message
      let errorMessage = 'An unknown error occurred during upload.';
      if (typeof err === 'object' && err !== null) {
          if ('response' in err && typeof err.response === 'object' && err.response !== null &&
              'data' in err.response && typeof err.response.data === 'object' && err.response.data !== null &&
              'detail' in err.response.data && typeof err.response.data.detail === 'string') {
              errorMessage = err.response.data.detail;
          } else if ('message' in err && typeof err.message === 'string') {
              errorMessage = err.message;
          }
      }
      setError(errorMessage);
      setIsUploading(false);
      if (onUploadError) {
        onUploadError(err as Error);
      }
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm bg-white dark:bg-gray-800 w-full max-w-md mx-auto">
      <h3 className="text-lg font-semibold mb-4 text-center">Upload File for Conversion</h3>

      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-md p-6 text-center cursor-pointer mb-4 ${isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'}`}
      >
        <input {...getInputProps()} />
        {selectedFile ? (
          <p>Selected: {selectedFile.name} ({Math.round(selectedFile.size / 1024)} KB)</p>
        ) : isDragActive ? (
          <p>Drop the file here ...</p>
        ) : (
          <p>Drag 'n' drop a file here, or click to select</p>
        )}
      </div>

      {selectedFile && (
        <div className="mb-4">
          <label htmlFor="outputFormat" className="block text-sm font-medium mb-1">Convert to:</label>
          <select
            id="outputFormat"
            value={selectedFormat}
            onChange={(e) => setSelectedFormat(e.target.value)}
            className="w-full p-2 border rounded-md bg-gray-50 dark:bg-gray-700 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500"
            disabled={isUploading}
          >
            {supportedOutputFormats.map(format => (
              <option key={format} value={format}>{format.toUpperCase()}</option>
            ))}
          </select>
        </div>
      )}

      {error && (
        <p className="text-red-500 dark:text-red-400 text-sm mb-4">Error: {error}</p>
      )}

      {isUploading && (
          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700 mb-4">
             {/* Basic indeterminate progress bar */}
             <div className="bg-blue-600 h-2.5 rounded-full animate-pulse"></div>
          </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isUploading ? 'Uploading...' : 'Upload and Convert'}
      </button>
    </div>
  );
} 