import React from 'react';

const Spinner = () => {
  return (
    <div className="flex justify-center items-center p-10">
      <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-cyan-400"></div>
      <p className="ml-4 text-xl text-gray-300">Analyzing Image...</p>
    </div>
  );
};

export default Spinner;