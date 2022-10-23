# Data

<!-- This folder contains ??. -->

<!-- TODO mention data collection notes, get_data.py script -->

## Accessing the raw data

Raw EEG data streamed from the OpenBCI GUI are available for 9 participants. EEG data and metadata are stored as Python dictionaries that have been serialized using the `pickle` module. Each `.pkl` file contains a dictionary with the following key-value pairs:

- `data`: 4-dimensional `numpy` array containing the EEG data. The array shape is: `(n_channels, n_samples, n_characters, n_blocks)`. For example, if a participant did 10 blocks of data collection using our 31-character keyboard with an 8-channel EEG device with a sampling frequency of 250 Hz, and if the stimulation duration is 5 seconds, the shape of the data will be `(8, 1250, 31, 10)`.
- `freq_type`: frequency configuration (`A`, `B`, `C`, or `D`). See `data_collection_notes.md` for details about the frequency-phase pairs used in each configuration.
- `freqs`: all frequencies (in Hz) associated with this frequency configuration, sorted in ascending order.
- `chars`: all characters associated with the frequencies in `freqs` (same order).

Here is an example showing how pickled data can be loaded in Python:

```{python}
import pickle

# this all blocks collected from participant S02 with frequency configuration A
# path assumes working directory is the data directory
path_data = 'raw/S02/S02_typeA.pkl' 

with open(path_data, 'rb') as file:
    data = pickle.load(file)

print(data.keys()) # dict_keys(['data', 'freq_type', 'freqs', 'chars'])
```

## EEG protocol

### Equipment

- 8-channel [OpenBCI Cyton board, dongle](https://shop.openbci.com/products/cyton-biosensing-board-8-channel), and batteries
- [Ten20 conductive paste](https://shop.openbci.com/products/ten20-conductive-paste-8oz-jar)
- Elastic headband <!-- TODO add dimensions -->
- Paintbrush and fabric paint

<!-- The data collected during the five seconds was then stored in the database and attributed to the cued key. This process iterated through each key on the keyboard with a 200 ms pause in between each one, completing one block of data collection. We aimed to acquire 10—15 blocks of data per participant. -->

To collect data from a participant, we first set up the necessary software. This included streaming live data using the OpenBCI GUI and opening the front and back ends. Meanwhile, the headband was placed on the participant's head using the aforementioned landmarks. The electrodes were then threaded through specific holes in the headband correlating to measured locations on the participant's head according to the 10/20 system. Two electrodes were additionally placed on both of the participant's ear lobes as the reference and bias electrodes. Figure 2 displays a sample electrode placement on one of the participants.

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/Sample%20Electode%20Set-Up.jpeg" width="500">

Figure 2: Sample Electrode Set-Up

The electrode positions were located by first measuring the distance between the nasion and the inion (d1) and the distance between the two ears (d2) using a measuring tape. The eight occipital electrode placements consisted of two rows, five on the bottom and three on the top. The two rows were marked by imaginary curves along 10% and 20% of d1 as measured from the inion. The five columns on the bottom row were marked by imaginary curves along 30%, 40%, 50%, 60%, and 70% of d2 as measured from one of the ears. The three columns on the top row were 40%, 50%, and 60% of d2. The electrodes were placed at the eight intersection points along the rows to achieve the Oz, O1, O2, PO7, PO8, POZ, PO3, and PO4 electrode positions of the 10/20 system.

Noise was limited to 8 microvolts for each electrode by limiting movement of the participant and of others in the vicinity. Data collection conditions were controlled for each participant by using the same electrode placements, positioning the participants around 40 cm from the keyboard display on the screen, and using the same hardware and environment conditions.

## Running the data collection interface

### OpenBCI GUI

### Data collection web app
