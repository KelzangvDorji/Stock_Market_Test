import React from 'react';

const HeroSection = () => {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl md:text-6xl font-bold mb-4">
        Market Risk Analysis
      </h1>
      <p className="text-xl text-neutral-300 mb-8">
        Real-time market data and risk assessment tools
      </p>
      <div className="flex justify-center gap-4">
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">
          Get Started
        </button>
        <button className="bg-neutral-700 hover:bg-neutral-600 text-white px-6 py-2 rounded-lg">
          Learn More
        </button>
      </div>
    </div>
  );
};

export default HeroSection; 