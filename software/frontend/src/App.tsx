import React, { useState } from 'react';
import './App.css';

import Keyboard from './components/Keyboard/Keyboard';
import InferenceView from './components/InferenceView';

function App() {
  const [chartData, setChartData] = useState<any[]>([]);
  const [useInference, setInference] = useState<boolean>(false);

  const [sentence, setSentence] = useState<string>("");
  const [autocompletePredictions, setAutocompletePredictions] = useState<string[]>(["option1", "option2", "option3"]);

  return (
    <div className='parent'>
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
                </div>

                <div className='rel'>
                  <Keyboard chartData={chartData} setChartData={setChartData} useInference={useInference} sentence={sentence} setSentence={setSentence} setAutocompletePredictions={setAutocompletePredictions} predictions={autocompletePredictions}/>

                  {useInference && <div className='abs'>
                  <InferenceView
                    label={sentence}
                    predictions={autocompletePredictions}
                    setSentence={setSentence}
                  />
                  </div>}
                </div>
    </div>
  );
}

export default App;
