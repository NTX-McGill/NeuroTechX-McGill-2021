# IRiSSE: Interfaced Recurrences in Steady-State Evocation

In this project, we built a speller that allows users to communicate by shifting their gaze to select characters on a flashing keyboard. It only requires users to be able to move their eyes, which could make it a useful tool for patients with disorders such as Locked-in syndrome or other forms of paralysis. 

Our speller relies on steady-state visually evoked potentials (SSVEPs), a type of signal that can be measured through electroencephalography (EEG). SSVEPs occur with specific types of visual stimuli such as flashing or flickering shapes: neurons in visual areas of the brain are entrained (their activity becomes synchronized) to the rhythm of the external stimulus. Flashing visual stimuli can be differentiated based on their frequencies. 

One of the benefits of SSVEPs is that they are passive signals: the user doesn't need to concentrate or learn how to produce them, which helps make our speller more accessible. 

Our speller has a keyboard layout where each key flashes with a different frequency-phase combination. We are able to identify the character the user is trying to select based on their EEG brain signals. We added autocompletion and next-word prediction features to help users type faster. In addition to the speller itself, we also built a data collection interface for recording and labelling EEG data from and SSVEP experiment. Our codebase and raw data are available in this repository. 

## Video presentation of the project

<!-- TODO add YouTube link/thumbnail -->

## Navigating the repository

<!-- TODO add links once merged to main -->

## Overview of the project

*Note*: The subfolders listed above contain more information about each component of the project, as well as instructions for installing and running our software and analyses.

### EEG data collection

We collected data from eleven university students, both male and female, with an 8-electrode set-up on the participant’s occipital lobe. The Oz, O1, O2, PO7, PO8, POZ, PO3, and PO4 electrode positions of the 10/20 system were used for data collection (Figure 1). To speed up the EEG setup time and help fix electrodes in place, we marked approximate locations for the eight 10/20 positions of interest on a headband. We placed the headband in a consistent way for all participants, using the inion, the top of the eyebrows and the helices of the pinnae (top of the ears) as landmarks. This way, we avoided having to measure each participant's head dimensions and had a more streamlined data collection process. 

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/10:20%20System%20Schematic.png" width="500">

Figure 1: 10/20 System Schematic

### Data collection platform

The data collection interface cued the participant to look at a specific key on the keyboard by highlighting it red. All keys would then flash at their unique frequencies and phases for five seconds. This process iterated randomly through each key on the keyboard with a 200 ms pause in between each one, completing one block of data collection. 

We experimented with different frequency configurations, finding that there was a range of frequencies that produced more easily identifiable SSVEP signals. Our final configuration consists of frequencies from 6.00–12.90 Hz incremented by 0.23 Hz, with phases starting at 0 and increasing by 0.35 $\pi$ radians. We mapped each frequency-phase pair to a key in our speller, making sure that keys that were physically close to each other would flash at frequencies that are more than 1 Hz apart.

<!-- TODO screenshot of data collection interface -->

### Signal processing

Electroencephalography (EEG) signals often require processing and filtering before relevant features can be extracted from them.

The main EEG frequencies are delta (0.5 to 4Hz), theta (4 to 7Hz), alpha (8 to 12Hz), and beta (13 to 30Hz). For our speller, visual flashing frequencies of interest lie in the 6-12.9 Hz range, corresponding mostly to alpha waves. The range was chosen after experimentation to maximize frequency spacing between letters while keeping the maximum frequency low to prevent aliasing.

To denoise our signal, we first apply a 60 Hz notch filter to remove the EMG noise. Then, to isolate frequencies of interest, we apply a 2nd order Chebyshev bandpass filter with a ripple of 0.3 dB to the range roughly corresponding to flashing frequencies (5.75-13.15Hz). We tuned hyperparameters to optimize performance. We experimented with signal smoothing and a procedure to reject channels based on an RMS threshold but found no significant performance benefits. In the end, we found only 1 channel is sufficient and best for our purposes.
### Signal classification

We use canonical correlation analysis (CCA) to find the oscillation frequency that most strongly correlates with our signal. The selected channels of the signal are passed into the algorithm with sine and cosine waves at a frequency matching each of the flashing keys. The sinusoid with highest correlation is chosen and the corresponding key is sent to software to be displayed and fed into the language model.
### Autocomplete/next-word prediction

Each time the user selects a letter on the keyboard, the language model gives the top 3 most likely word completions. The model was trained on TV transcripts by learning the frequencies between pairs of words and single words. TV transcripts provide good information for natural language and discussion. 

By incorporating a natural language model into our BCI ecosystem, we are able to speed up the about of information communicated and handle errors that would otherwise lead to miscommunication.

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/spellerTest.png" width="500" >

### Spelling/inference platform

### Limitations and future directions

## Partners

* [Building 21](https://building21.ca/)

## About us

We are an interdisciplinary group of dedicated undergraduate students from McGill University and our mission is to raise awareness and interest in neurotechnology, biosignals and human-computer interfaces. For more information, see our [Facebook page](https://www.facebook.com/McGillNeurotech).
