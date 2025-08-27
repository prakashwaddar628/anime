import React from 'react';

const SimilarCharactersList = ({ characters }) => {
  // Handle case where there are no similar characters
  if (!characters || characters.length === 0) {
    return <p className="text-gray-400">No similar characters found.</p>;
  }

  return (
    <div>
      <h3 className="text-2xl font-bold text-cyan-300 mb-4">Similar Characters</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {characters.map((char, index) => (
          <div key={index} className="bg-gray-700 rounded-lg overflow-hidden shadow-lg transition-transform transform hover:scale-105">
            {char.image_url ? (
              <img src={char.image_url} alt={char.name} className="w-full h-75 object-cover" />
            ) : (
              <div className="w-full h-48 bg-gray-600 flex items-center justify-center">
                <p className="text-gray-400">No Image</p>
              </div>
            )}
            <div className="p-3">
              <h4 className="font-bold text-lg text-white truncate">{char.name}</h4>
              <p className="text-sm text-gray-400 truncate">{char.anime}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SimilarCharactersList;