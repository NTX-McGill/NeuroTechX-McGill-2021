# SSVEP Speller

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

### Data collection

We collected data from eleven university students, both male and female, with an 8-electrode set-up on the participant’s occipital lobe. The Oz, O1, O2, PO7, PO8, POZ, PO3, and PO4 electrode positions of the 10/20 system were used for data collection (Figure 1). The electrodes were fixed in position with a headband using the nasion, inion, and the helices of the pinnae as landmarks. Noise was limited to 8 microvolts for each electrode by limiting movement of the participant and of others in the vicinity. Data collection conditions were controlled for each participant by using the same electrode placements, positioning the participants around 40 cm from the keyboard display on the screen, and using the same hardware and environment conditions.

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/10:20%20System%20Schematic.png" width="500">

Figure 1: 10/20 System Schematic

The data collection interface cued the participant to look at a specific key on the keyboard by highlighting it red. All keys would then flash at their unique frequencies and phases for five seconds. Frequencies varied from 6.00–12.90 Hz incremented by 0.23 Hz while the phases started at 0 and increased by 0.35 pi radians. The data collected during the five seconds was then stored in the database and attributed to the cued key. This process iterated through each key on the keyboard with a 200 ms pause in between each one, completing one block of data collection. We aimed to acquire 10—15 blocks of data per participant.

<!-- TODO screenshot of data collection interface -->

To collect data from a participant, we first set up the necessary software. This included streaming live data using the OpenBCI GUI and opening the front and back ends. Meanwhile, the headband was placed on the participant's head using the aforementioned landmarks. The electrodes were then threaded through specific holes in the headband correlating to measured locations on the participant's head according to the 10/20 system. Two electrodes were additionally placed on both of the participant's ear lobes as the reference and bias electrodes. Figure 2 displays a sample electrode placement on one of the participants.

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/Sample%20Electode%20Set-Up.jpeg" width="500">

Figure 2: Sample Electrode Set-Up

The electrode positions were located by first measuring the distance between the nasion and the inion (d1) and the distance between the two ears (d2) using a measuring tape. The eight occipital electrode placements consisted of two rows, five on the bottom and three on the top. The two rows were marked by imaginary curves along 10% and 20% of d1 as measured from the inion. The five columns on the bottom row were marked by imaginary curves along 30%, 40%, 50%, 60%, and 70% of d2 as measured from one of the ears. The three columns on the top row were 40%, 50%, and 60% of d2. The electrodes were placed at the eight intersection points along the rows to achieve the Oz, O1, O2, PO7, PO8, POZ, PO3, and PO4 electrode positions of the 10/20 system.

<!-- TODO add picture -->

### Signal processing

### Signal classification

### Autocomplete/next-word prediction

### Data collection platform

### Spelling/inference platform

### Limitations and future directions

## Partners

* [Building 21](https://building21.ca/)

## About us

We are an interdisciplinary group of dedicated undergraduate students from McGill University and our mission is to raise awareness and interest in neurotechnology, biosignals and human-computer interfaces. For more information, see our [Facebook page](https://www.facebook.com/McGillNeurotech).
