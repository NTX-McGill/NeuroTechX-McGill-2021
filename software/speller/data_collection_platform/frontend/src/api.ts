import axios from 'axios'

var URL = "http://localhost:5000/api"

export async function startBCI() {
    var path = "/openbci/start"
    const response = await fetch(`${URL}${path}`, {
        method: 'POST',
    });
    return await response.json();
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
    var bodyFormData = new FormData();

    bodyFormData.append('character', key)
    bodyFormData.append('frequency', freq.toString())
    bodyFormData.append('phase', phase.toString())

    return await axios.post(`${URL}${path}`, bodyFormData)
    //return await response.json();
}

export async function stopCollectingKey(processID: number) {
    var path = `/openbci/${processID}/collect/stop`
    const response = await fetch(`${URL}${path}`, {
        method: 'POST',
    });
    return await response.json();
}