#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  26 12:14:21 2021

@author: steve
"""
import numpy as np
from filter import SAMPLE_RATE
import filter
from filter import load_ecg,filter_signal_mne_uniform_band
from scipy.signal import find_peaks


def ecg_detect_rpeaks_basic(filtered_signal,drop_first=True):
    """
    This is a 'off the top of my head' algorithm that needs to be improved.

    input
        1D numpy array ECG signal
        
    output
        1D array of times (in seconds) at which an R peak was achieved
    """
    # square the signal
    squared_signal = filtered_signal**2
    # the high cutoff threshold is determined by the maximum value of the array, 
    # the filtering artifact appears to be shorter than 50 indices
    thresh = np.max(filtered_signal[100:-1000])/3.0 # cutoff last four seconds too
    # this threshold is just eyeballed
    high_indices = np.array([t for t,s in enumerate(squared_signal) if s>thresh**2])
    r_times = [] # list of timestamps at which the r peak is attained
    for i,j in zip(high_indices[1:],high_indices[1:]-high_indices[:-1]):
        if j > SAMPLE_RATE / 10:
            # i is the index of the 'beginning' of the peak
            peak_idx = i + np.argmax(squared_signal[i:i+int(SAMPLE_RATE/10)])
            r_times.append(peak_idx / SAMPLE_RATE)

    if drop_first:
        r_times = r_times[1:] # discard the first entry due to filtering artifact 
    return np.array(r_times)
    
def ecg_detect_qrs(filtered_signal):
    """
    input
        1D filtered ECG signal
    output
        2D array in format [[q1,r1,s1], [q2,r2,s2], ...etc. ]
    """
    # square the signal
    squared_signal = filtered_signal**2
    thresh = np.max(filtered_signal[100:-1000]) / 3.0 # assumes at least 5 seconds long
    high_indices = np.array([t for t,s in enumerate(squared_signal) if s>thresh**2])
    qrs_indices = []
    for i,j in zip(high_indices[1:],high_indices[1:]-high_indices[:-1]):
        if j > SAMPLE_RATE / 10:
            # i is the index of the 'beginning of the peak'
            qrs_idx, _ = find_peaks(squared_signal[i-int(SAMPLE_RATE/10):i+int(SAMPLE_RATE/10)])
            qrs_idx += i - int(SAMPLE_RATE/10)
            if len(qrs_idx) == 3:
                qrs_indices.append(qrs_idx)
                print("3",end="\t")# trace
            elif len(qrs_idx) > 3:
                print("geq3",end="\n")# trace
                qrs_idx_new = []
                while len(qrs_idx_new) < 3:
                    argmax = np.argmax(squared_signal[qrs_idx])
                    qrs_idx_new.append(qrs_idx[argmax])
                    qrs_idx = np.delete(qrs_idx,argmax)
                # to put them in order we note that Q is the smallest, followed by S and R tallest
                qrs_indices.append(np.array([qrs_idx_new[2],qrs_idx_new[0],qrs_idx_new[1]])) 
            else:
                print("\npeak detection error!")# trace
    return np.array(qrs_indices)



def hrv_time_domain(filtered_signal):
    """
    input - filtered ECG signal
    output - the hrv score (heart-rate variability)
    """
    r_times = ecg_detect_rpeaks_basic(filtered_signal) 
    rr_intervals = r_times[1:] - r_times[:-1]
    rr_interval_diffs = rr_intervals[1:] - rr_intervals[:-1]
    hrv = np.sqrt(np.mean(rr_interval_diffs**2))
    return hrv 

"""
# test ecg_detet_rpeaks_basic() and hrv_time_domain()
if __name__ == "__main__":
    file_path = "../data/2021-05-20/01-1_video_OpenBCI-RAW-2021-05-20_19-59-47.txt"
    raw_signal = filter.load_ecg(file_path)
    filtered_signal = np.squeeze(filter_signal_mne_uniform_band(np.array([raw_signal])))
    r_peak_times = ecg_detect_rpeaks_basic(filtered_signal)
    print("\nr_peak_times\n{}".format(r_peak_times))
    hrv = hrv_time_domain(filtered_signal)
    print("\nHeart Rate Variability = {}".format(hrv)) 
    print("\n\nGoodbye!")
"""

# test ecg_detect_qrs()
if __name__ == "__main__":
    file_path = "../data/2021-05-20/01-1_video_OpenBCI-RAW-2021-05-20_19-59-47.txt"
    raw_signal = filter.load_ecg(file_path)
    filtered_signal = np.squeeze(filter_signal_mne_uniform_band(np.array([raw_signal])))
    filtered_signal = filtered_signal[100:-100] # trim the signal
    filtered_signal = filtered_signal[:SAMPLE_RATE * 10] # ten seconds for visual purposes
    qrs_idxs = ecg_detect_qrs(filtered_signal)
    q_idxs = qrs_idxs.T[0]
    r_idxs = qrs_idxs.T[1]
    s_idxs = qrs_idxs.T[2]
    r_idxs_original = ecg_detect_rpeaks_basic(filtered_signal,drop_first=False)

    print("comparing r_times:")
    count=0
    for i,j in zip(r_idxs/250,r_idxs_original):
        if np.round(i,3)==np.round(j,3):
            print("True",end=" ")
        else:
            count+=1
            print("\n\nFalse: i,j = {},{}".format(i,j))
    print("\ncount = {}".format(count))

    # print(r_idxs/250)
    # print(r_idxs_original)

    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,4))
    plt.plot(filtered_signal,label="filtered_signal")
    plt.plot(r_idxs,filtered_signal[r_idxs],"x",label="r")
    plt.plot(s_idxs,filtered_signal[s_idxs],"x",label="s")
    plt.plot(q_idxs,filtered_signal[q_idxs],"x",label="q")
    plt.legend()
    plt.show()
    


