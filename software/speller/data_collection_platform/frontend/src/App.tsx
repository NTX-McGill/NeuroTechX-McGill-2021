import React, { useState } from 'react';
import './App.css';
import Keyboard from './components/Keyboard/Keyboard';
import LineGraph from './components/LineGraph';

function App() {
  const [chartData, setChartData] = useState<any[]>([]);

  return (
    <div className="container">
      <div className={'grid-item'}>
        <h1>Speller</h1>
        <h3>Data Collection Platform</h3>
      </div>
      <div className={'grid-item'}>
        <Keyboard chartData={chartData} setChartData={setChartData} />
      </div>
      <div className={'grid-item'}>
        <LineGraph data={chartData} />
      </div>
    </div>
  );
}

export default App;
