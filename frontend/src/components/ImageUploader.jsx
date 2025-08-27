import React from 'react';

const ImageUploader = ({ selectedFile, previewUrl, handleFileChange, handleUpload, isLoading }) => {
  return (
    <div className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-cyan-500 rounded-lg">
      <h2 className="text-2xl font-semibold mb-4 text-gray-200">Upload Character Image</h2>
      
      <div className="w-full max-w-xs mb-4">
        <input
          type="file"
          onChange={handleFileChange}
          accept="image/*"
          className="block w-full text-sm text-gray-400
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-cyan-600 file:text-white
            hover:file:bg-cyan-700"
        />
      </div>

      {previewUrl && (
        <div className="mb-4">
          <h3 className="text-lg font-medium text-gray-300 mb-2">Image Preview:</h3>
          <img src={previewUrl} alt="Selected character" className="max-w-xs h-auto rounded-lg shadow-lg" />
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!selectedFile || isLoading}
        className="px-6 py-2 bg-green-500 text-white font-bold rounded-lg hover:bg-green-600 disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Recognizing...' : 'Recognize Character'}
      </button>
    </div>
  );
};

export default ImageUploader;