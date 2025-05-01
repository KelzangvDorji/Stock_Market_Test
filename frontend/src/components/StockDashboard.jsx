import React from 'react';
import StockGraph from './graph';

const StockDashboard = () => {
  return (
    <div className="bg-neutral-800 rounded-lg p-6 shadow-lg mb-8">
      <h2 className="text-2xl font-bold mb-4">Stock Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-neutral-700 p-4 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Market Overview</h3>
          <StockGraph />
        </div>
        <div className="bg-neutral-700 p-4 rounded-lg">
          <h3 className="text-xl font-semibold mb-2">Portfolio Summary</h3>
          <p className="text-neutral-300">Your portfolio performance metrics</p>
        </div>
      </div>
    </div>
  );
};

export default StockDashboard; 