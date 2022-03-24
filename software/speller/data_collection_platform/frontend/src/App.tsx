import React, { useState } from 'react';
import './App.css';

import Keyboard from './components/Keyboard/Keyboard';
import InferenceView from './components/InferenceView';

function App() {
  const [chartData, setChartData] = useState<any[]>([]);
  const [useInference, setInference] = useState<boolean>(false);

  return (
    <div className="container">
      <div className={'grid-item'}>
        <h1>Speller</h1>
        <div className={'mode'}>
          <h3>
            {useInference ? 'Inference Platform' : 'Data Collection Platform'}
          </h3>
          <button onClick={() => setInference(!useInference)}>
            {useInference ? 'Go to Data Collection' : 'Go to Inference'}
          </button>
        </div>
      </div>
      {useInference ? (
        <div className={'col-container'}>
          <Keyboard chartData={chartData} setChartData={setChartData} />
          <InferenceView
            label={'testing hello this is a long sentence, I need to make sure it can wrap. adf asdf adf adsf asdf asdf asdf asdf  asdf asdf asdf asdf asdf asdf '}
            predictions={[
              { value: 'a', confidence: 0.9 },
              { value: 'b', confidence: 0.8 },
            ]}
          />
        </div>
      ) : (
        <div className={'grid-item'}>
          <Keyboard chartData={chartData} setChartData={setChartData} />
        </div>
      )}
    </div>
  );
}

export default App;
