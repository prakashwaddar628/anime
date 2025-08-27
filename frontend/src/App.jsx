import React, { useState } from "react";
import ImageUploader from "./components/ImageUploader";
import Spinner from "./components/Spinner";
// We will create ResultsDisplay later, so we comment it out for now
import ResultsDisplay from "./components/ResultsDisplay";

function App() {
  // State for the selected image file
  const [selectedFile, setSelectedFile] = useState(null);
  // State for the image preview URL
  const [previewUrl, setPreviewUrl] = useState("");
  // State to hold the API response data
  const [result, setResult] = useState(null);
  // State to manage loading status
  const [isLoading, setIsLoading] = useState(false);
  // State to hold any error messages
  const [error, setError] = useState("");

  const API_URL = "http://127.0.0.1:8000/recognize";

  // --- HANDLER FUNCTIONS ---

  // Handles the file selection from the input
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Create a URL for the image preview
      setPreviewUrl(URL.createObjectURL(file));
      // Reset previous results/errors
      setResult(null);
      setError("");
    }
  };

  // Handles the "Recognize" button click and calls the backend
  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    // Start loading and clear previous error
    setIsLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        // If the server response is not OK, parse the error detail
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! Status: ${response.status}`
        );
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("API Call failed:", err);
      setError(err.message || "An unknown error occurred.");
    } finally {
      // Stop loading regardless of success or failure
      setIsLoading(false);
    }
  };

  // Resets the state to allow for a new search
  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl("");
    setResult(null);
    setError("");
  };

  // --- RENDER LOGIC ---

  return (
    <div className="bg-gray-900 min-h-screen text-white p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-cyan-400 mb-2">
            Anime Character Recognizer
          </h1>
          <p className="text-md text-gray-400">
            Upload an image to identify a character and find similar ones.
          </p>
        </header>

        <main className="bg-gray-800 p-6 rounded-xl shadow-2xl">
          {/* Conditional rendering based on the app's state */}

          {isLoading ? (
            <Spinner />
          ) : error ? (
            <div className="text-center">
              <p className="text-red-400 font-semibold mb-4">{error}</p>
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-cyan-600 rounded-lg"
              >
                Try Again
              </button>
            </div>
          ) : result ? (
            <div>
              <ResultsDisplay result={result} />
              <div className="text-center mt-8">
                <button
                  onClick={handleReset}
                  className="px-6 py-2 bg-cyan-600 text-white font-bold rounded-lg hover:bg-cyan-700 transition-colors"
                >
                  Recognize Another Character
                </button>
              </div>
            </div>
          ) : (
            <ImageUploader
              selectedFile={selectedFile}
              previewUrl={previewUrl}
              handleFileChange={handleFileChange}
              handleUpload={handleUpload}
              isLoading={isLoading}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
