import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { fileService } from '../services/fileService';
import { useAuthStore } from '../store'; // To check if user is logged in

const HomePage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [outputFormat, setOutputFormat] = useState<string>('pdf'); // Default output format
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setUploadMessage(null);
    setErrorMessage(null);
    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0]);
      console.log('File selected:', acceptedFiles[0].name);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } =
    useDropzone({
      onDrop,
      multiple: false, // Allow only single file upload
      // TODO: Add file type restrictions based on supported formats
      // accept: { 'image/jpeg': [], 'image/png': [], 'application/pdf': [] }
    });

  const handleUpload = async () => {
    if (!selectedFile) {
      setErrorMessage('Please select a file first.');
      return;
    }
    if (!isAuthenticated) {
        setErrorMessage('Please log in to upload files.');
        return;
    }

    setIsUploading(true);
    setUploadMessage(null);
    setErrorMessage(null);

    try {
      const response = await fileService.uploadFile(selectedFile, outputFormat);
      setUploadMessage(`${response.message} Task ID: ${response.task_id}`);
      setSelectedFile(null); // Clear selection after successful upload queue
    } catch (error: unknown) {
        console.error('Upload error:', error);
         let errorMsg = "File upload failed. Please try again.";
         if (typeof error === 'object' && error !== null && 'response' in error) {
            const axiosError = error as { response?: { data?: { detail?: string } } };
            errorMsg = axiosError.response?.data?.detail || errorMsg;
        }
      setErrorMessage(errorMsg);
    } finally {
      setIsUploading(false);
    }
  };

  // TODO: Define actual supported output formats
  const supportedOutputFormats = ['pdf', 'docx', 'txt', 'jpg', 'png', 'mp3'];

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6 text-center">Universal File Converter</h1>

      {!isAuthenticated && (
          <div className="mb-4 p-3 bg-yellow-100 border border-yellow-400 text-yellow-800 rounded text-center">
             Please log in to use the file converter.
          </div>
      )}

      <div
        {...getRootProps()}
        className={`p-10 border-2 border-dashed rounded-lg text-center cursor-pointer
                   ${isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-gray-700' : 'border-gray-300 dark:border-gray-600'}
                   hover:border-blue-400 transition duration-200`}
      >
        <input {...getInputProps()} />
        {selectedFile ? (
          <p>Selected file: {selectedFile.name}</p>
        ) : isDragActive ? (
          <p>Drop the file here ...</p>
        ) : (
          <p>Drag 'n' drop a file here, or click to select file</p>
        )}
      </div>

      {selectedFile && (
        <div className="mt-6 flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <div className="flex-grow sm:flex-grow-0">
            <label htmlFor="outputFormat" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Convert to:
            </label>
            <select
              id="outputFormat"
              value={outputFormat}
              onChange={(e) => setOutputFormat(e.target.value)}
              className="w-full sm:w-auto px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
            >
              {supportedOutputFormats.map(format => (
                  <option key={format} value={format}>{format.toUpperCase()}</option>
              ))}
            </select>
          </div>
          <button
            onClick={handleUpload}
            disabled={isUploading || !isAuthenticated}
            className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ease-in-out disabled:opacity-50"
          >
            {isUploading ? 'Uploading...' : 'Start Conversion'}
          </button>
        </div>
      )}

      {uploadMessage && (
        <div className="mt-4 p-3 bg-green-100 border border-green-400 text-green-800 rounded text-center">
          {uploadMessage}
        </div>
      )}
      {errorMessage && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded text-center">
          {errorMessage}
        </div>
      )}

        {/* TODO: Add section to display conversion history/status */}
    </div>
  );
};

export default HomePage; 