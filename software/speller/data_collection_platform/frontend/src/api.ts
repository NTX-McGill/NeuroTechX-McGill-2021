import axios from 'axios';

var URL = 'http://localhost:5000/api';

export async function startBCI(collectorName?: string) {
  var path = '/openbci/start';
  return await axios.post(`${URL}${path}`, {
    collector_name: collectorName ? collectorName : "",
  });
}

export async function stopBCI(processID: number) {
  var path = `/openbci/${processID}/stop`;
  return await axios.post(`${URL}${path}`);
}

export async function startCollectingKey(
  processID: number,
  predict: boolean,
  key?: string,
  phase?: number,
  freq?: number
) {
  var path = `/openbci/${processID}/collect/start`;

    return await axios.post(`${URL}${path}`, {
      predict: predict,
      character: key,
      frequency: freq?.toString(),
      phase: phase?.toString(),
    });
}

export async function stopCollectingKey(processID: number, predict: boolean, sentence?: string) {
  var path = `/openbci/${processID}/collect/stop`;

  /*
  const response = await fetch(`${URL}${path}`, {
    method: 'POST',
    body: JSON.stringify({predict: predict})
  });
  return await response.json();
  */

  return await axios.post(`${URL}${path}`, {
    predict: predict,
    sentence: sentence,
  });
}