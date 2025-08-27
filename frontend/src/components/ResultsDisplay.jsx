import React from 'react';
import SimilarCharactersList from './SimilarCharactersList';

const ResultsDisplay = ({ result }) => {
  const { prediction_result, character_details, similar_characters } = result;

  return (
    <div className="space-y-8">
      {/* Main Character Display */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 bg-gray-700 p-6 rounded-lg">
        <div className="md:col-span-1 flex justify-center">
          <img
            src={character_details.image_url || 'https://via.placeholder.com/300x450'}
            alt={character_details.name}
            className="rounded-lg shadow-xl w-full max-w-xs object-cover"
          />
        </div>

        <div className="md:col-span-2 space-y-4">
          <h2 className="text-3xl font-bold text-white">{character_details.name}</h2>
          <p className="text-lg text-gray-300">
            from <span className="font-semibold text-cyan-400">{character_details.anime_name}</span>
          </p>
          <div className="text-sm font-semibold text-green-400 bg-green-900/50 inline-block px-3 py-1 rounded-full">
            Confidence: {prediction_result.confidence}
          </div>

          <div>
            <h4 className="font-semibold text-gray-200 mb-2">About:</h4>
            <p className="text-gray-400 text-base">{character_details.about}</p>
          </div>

          <div>
            <h4 className="font-semibold text-gray-200 mb-2">Appearance Tags:</h4>
            <div className="flex flex-wrap gap-2">
              {character_details.tags.map((tag, index) => (
                <span key={index} className="bg-gray-600 text-gray-200 text-xs font-medium px-2.5 py-1 rounded-full">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-200 mb-2">Where to Watch:</h4>
            <div className="flex flex-wrap gap-2">
              {character_details.streaming_platforms.length > 0 ? (
                character_details.streaming_platforms.map((platform, index) => (
                  <span key={index} className="bg-cyan-800 text-cyan-200 text-sm font-semibold px-3 py-1 rounded-md">
                    {platform}
                  </span>
                ))
              ) : (
                <p className="text-gray-500">Not available on major platforms.</p>
              )}
            </div>
          </div>

        </div>
      </div>
      
      {/* Similar Characters Section */}
      <SimilarCharactersList characters={similar_characters} />
    </div>
  );
};

export default ResultsDisplay;