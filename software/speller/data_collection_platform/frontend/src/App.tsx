import React, { useState } from 'react';
import './App.css';

import Keyboard from './components/Keyboard/Keyboard';
import InferenceView from './components/InferenceView';

function App() {
  const [chartData, setChartData] = useState<any[]>([]);
  const [useInference, setInference] = useState<boolean>(false);

  const [sentence, setSentence] = useState<string>("sentence");

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
        {useInference && <div className={'inference-div'}>
        <InferenceView
            label={sentence}
            predictions={[
              { value: 'a', confidence: 0.9 },
              { value: 'b', confidence: 0.8 },
            ]}
          />
        </div>}
      </div>
      {useInference ? (
        <div className={'grid-item'}>
          <Keyboard chartData={chartData} setChartData={setChartData} useInference={useInference} setSentence={setSentence}/>
        </div>
      ) : (
        <div className={'grid-item'}>
          <Keyboard chartData={chartData} setChartData={setChartData} useInference={useInference} setSentence={setSentence}/>
        </div>
      )}
    </div>
  );
}

export default App;
