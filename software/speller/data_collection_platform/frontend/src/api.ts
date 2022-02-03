import axios from 'axios'

var URL = "http://localhost:5000/api"

export async function startBCI(collectorName: string) {
    var path = "/openbci/start"
    return await axios.post(`${URL}${path}`, {
        collector_name: collectorName
    })
}

export async function stopBCI(processID: number) {
    var path = `/openbci/${processID}/stop`
    const response = await fetch(`${URL}${path}`, {
        method: 'POST',
    });
    return await response.json();
}

export async function startCollectingKey(processID: number, key: string, phase: number, freq: number) {
    var path = `/openbci/${processID}/collect/start`
    /*
    const response = await fetch(`${URL}${path}`, {
        method: 'POST',
        body: JSON.stringify({
            character: key,
            frequency: freq,
            phase: phase
        })
    });
    */
    return await axios.post(`${URL}${path}`, {
        character: key,
        frequency: freq.toString(),
        phase: phase.toString()
    })
    //return await response.json();
}

export async function stopCollectingKey(processID: number) {
    var path = `/openbci/${processID}/collect/stop`
    const response = await fetch(`${URL}${path}`, {
        method: 'POST',
    });
    return await response.json();
}