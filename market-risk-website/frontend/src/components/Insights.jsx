import React from 'react';

const Insights = () => {
  return (
    <div className="bg-neutral-800 rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Market Insights</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-neutral-700 p-4 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Trend Analysis</h3>
          <p className="text-neutral-300">Analyze market trends and patterns</p>
        </div>
        <div className="bg-neutral-700 p-4 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Risk Assessment</h3>
          <p className="text-neutral-300">Evaluate portfolio risk factors</p>
        </div>
      </div>
    </div>
  );
};

export default Insights; 