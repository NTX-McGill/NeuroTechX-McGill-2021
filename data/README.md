# Data

We collected data from eleven university students, both male and female, with an 8-electrode set-up on the participant’s occipital lobe. The Oz, O1, O2, PO7, PO8, POZ, PO3, and PO4 electrode positions of the 10/20 system were used for data collection (Figure 1). The electrodes were fixed in position with a headband using the nasion, inion, and the helices of the pinnae as landmarks. Noise was limited to 8 microvolts for each electrode by limiting movement of the participant and of others in the vicinity. Data collection conditions were controlled for each participant by using the same electrode placements, positioning the participants around 40 cm from the keyboard display on the screen, and using the same hardware and environment conditions.

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/10:20%20System%20Schematic.png" width="500">

Figure 1: 10/20 System Schematic

The data collection interface cued the participant to look at a specific key on the keyboard by highlighting it red. All keys would then flash at their unique frequencies and phases for five seconds. Frequencies varied from 6.00–12.90 Hz incremented by 0.23 Hz while the phases started at 0 and increased by 0.35 pi radians. The data collected during the five seconds was then stored in the database and attributed to the cued key. This process iterated through each key on the keyboard with a 200 ms pause in between each one, completing one block of data collection. We aimed to acquire 10—15 blocks of data per participant.

To collect data from a participant, we first set up the necessary software. This included streaming live data using the OpenBCI GUI and opening the front and back ends. Meanwhile, the headband was placed on the participant's head using the aforementioned landmarks. The electrodes were then threaded through specific holes in the headband correlating to measured locations on the participant's head according to the 10/20 system. Two electrodes were additionally placed on both of the participant's ear lobes as the reference and bias electrodes. Figure 2 displays a sample electrode placement on one of the participants.

<img src="https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/cleanup/img/Sample%20Electode%20Set-Up.jpeg" width="500">

Figure 2: Sample Electrode Set-Up

The electrode positions were located by first measuring the distance between the nasion and the inion (d1) and the distance between the two ears (d2) using a measuring tape. The eight occipital electrode placements consisted of two rows, five on the bottom and three on the top. The two rows were marked by imaginary curves along 10% and 20% of d1 as measured from the inion. The five columns on the bottom row were marked by imaginary curves along 30%, 40%, 50%, 60%, and 70% of d2 as measured from one of the ears. The three columns on the top row were 40%, 50%, and 60% of d2. The electrodes were placed at the eight intersection points along the rows to achieve the Oz, O1, O2, PO7, PO8, POZ, PO3, and PO4 electrode positions of the 10/20 system.
