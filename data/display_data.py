#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  26 12:29:24 2021

@author: steve
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../signal/')
from filter import load_virgin_file,filter_signal_mne_8chan,SAMPLE_RATE

file_path = sys.argv[1] # this is the path to an OpenBci raw data file (.txt) input by the user

print("Displaying all channels in \n'{}'".format(file_path))

data = load_virgin_file(file_path)
print(data.shape)
print(data.T[0][:100])

# filter the signals as usual
filtered = filter_signal_mne_8chan(data.T)

window_length = 2.0 # in seconds, the length of window to display on right column

# display each channel, the whole signal on left column, a short window on right column
plt.subplots()
for n,ts in enumerate(filtered):
    plt.subplot(8,2,2*n+1)
    plt.plot(np.arange(len(ts[100:]))/SAMPLE_RATE , ts[100:]) # index 100 to remove filtering artifact
    plt.xlabel("Time in seconds")
    plt.ylabel("Micro Volts")
    plt.title("Filtered signal    Channel {}".format(n+1),fontsize=11)
    plt.subplot(8,2,2*n+2)
    window = ts[100:100 + int(SAMPLE_RATE * window_length)]
    plt.plot(np.arange(len(window))/SAMPLE_RATE , window)
    plt.xlabel("Time in seconds")
    plt.ylabel("Micro Volts")
    plt.title("a {} second sample    Channel {}".format(window_length,n+1),fontsize=11)

plt.tight_layout()
plt.show()