import React, { useState } from 'react';
import './App.css';
import Keyboard from './components/Keyboard/Keyboard';

function App() {
  const [chartData, setChartData] = useState<any[]>([]);
  const [name, setName] = useState<string>('');

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
        <form>
          <label>
            Collector name
            <br />
            <input value={name} onChange={e => setName(e.target.value)} />
          </label>
        </form>
      </div>
    </div>
  );
}

export default App;
