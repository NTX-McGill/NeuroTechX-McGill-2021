#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  26 11:09:43 2021

@author: steve
"""
import numpy as np
import matplotlib.pyplot as plt
import mne
from scipy.signal import butter, filtfilt

SAMPLE_RATE = 250  # Hz
REVERSE_SIGNAL = True  # voltage reversed in some samples TODO determine programmatically
CONVERT_TO_VOLTS = True  # /voltage by 1000 for readability

def load_virgin_file(file_path,channels=[1,2,3,4,5,6,7,8]):
    """
    loads a raw OpenBci output textfile into a 2D numpy array
    """
    data = np.loadtxt(file_path,
                        delimiter=",",
                        skiprows=7,
                        usecols=channels)
    return data

def load_ecg(file_path):
    # loads just the heartbeats channel
    return load_virgin_file(file_path,channels=[1])

def butter_filter(data, cutoff, order, btype):
    """
    Applies the Butterworth filter to 2D array of signals dim: nchan * len_timeseries

    Input:
    - data : 2D array of raw signals from ECG or EEG
    - cutoff : cutoff frequency
    - order : order at which to apply filter
    - btype : filter type; 'lowpass' or 'highpass'

    Output:
        2D array of filtered signals from ECG or EEG
    """
    [b,a] = butter(order, cutoff, btype=btype, analog=False)
    return filtfilt(b, a, data, padlen=3*(max(len(b),len(a))-1))

def filter_ecg(data, lowpass=0.17,lp_order=6,highpass=0.01,hp_order=3):
    """
    Filters 1D array of signals dim: len_timeseries

    Input:
    - data : 1D array of raw signals from ECG
    - lowpass : frequencies below this are discarded
    - lp_order : order for the lowpass Butterworth filter
    - highpass : frequencies above this are discarded
    - hp_order : order for the highpass Butterworth filter

    Output:
        1D array, filtered ECG signal to remove noise
    """

    # Configurations
    initial_samples_to_trim = 100  # trimmed after filtering to remove filter artifacts

    # Correct the signal
    if REVERSE_SIGNAL:
        data = (-data + np.max(data))
    if CONVERT_TO_VOLTS:
        data /= 1000

    # Normalize the data
    n_samples = data.shape[0]
    time = np.array(range(n_samples)) / SAMPLE_RATE
    fit = np.polyfit(time, data, 1)
    normalized_data = data - (fit[0] * time + fit[1])

    # Apply the lowpass filter
    lp_filtered_data = butter_filter(normalized_data, lowpass, lp_order, 'lowpass')
    
    # Apply the highpass filter
    filtered_data = butter_filter(lp_filtered_data, highpass, hp_order, 'highpass')

    # Trim the beginning to remove any filter artifacts
    return filtered_data[initial_samples_to_trim:]

def filter_qrs(data,lowpass=0.016,lp_order=5,highpass=0.001,hp_order=4):
    """
    Filters 1D array of signals dim: len_timeseries

    Input:
    - data : 1D array of raw signals from ECG
    - lowpass : frequencies below this are discarded
    - lp_order : order for the lowpass Butterworth filter
    - highpass : frequencies above this are discarded
    - hp_order : order for the highpass Butterworth filter

    Output:
        1D array, filtered ECG signal to have exactly one peak for each QRS complex
    """

    # Configurations
    initial_samples_to_trim = 100  # trimmed after filtering to remove filter artifacts

    # Correct the signal
    if REVERSE_SIGNAL:
        data = (-data + np.max(data))
    if CONVERT_TO_VOLTS:
        data /= 1000

    # Normalize the data
    n_samples = data.shape[0]
    time = np.array(range(n_samples)) / SAMPLE_RATE
    fit = np.polyfit(time, data, 1)
    normalized_data = data - (fit[0] * time + fit[1])

    # Apply the lowpass filter
    lp_filtered_data = butter_filter(normalized_data, lowpass, lp_order, 'lowpass')
    
    # Apply the highpass filter
    filtered_data = butter_filter(lp_filtered_data, highpass, hp_order, 'highpass')

    # Trim the beginning to remove any filter artifacts
    return filtered_data[initial_samples_to_trim:]

def filter_signal_mne_uniform_band(data,bp_lowcut=8,bp_highcut=20):
    """
    Filters 2D array of signals dim: nchan x len_timeseries

    Input:
    - data : 2D array of raw signals from EEG and ECG
    - bp_lowcut : units of Hz - frequencies below this are discarded 
    - bp_highcut : units of Hz - frequencies above this are discarded

    Output:
        2D array, filtered signal (EEG and ECG), all filtered with same params

    The default parameters for the bandpass filter are optimized for ECG, 
    we will have to change this when we get EEG data. For info on optimal params see:
    https://www.researchgate.net/publication/307615951_Selection_of_Parameters_of_Bandpass_Filtering_of_the_ECG_Signal_for_Heart_Rhythm_Monitoring_Systems
    """

    # bp_order = 2
    # notch_order = 2 # bp_order and notch_order is for numpy filters only...
    notch_freq_Hz = [60.0,120.0] 
    
    filtered = data
    # notch filter
    filtered = np.apply_along_axis(lambda l:mne.filter.notch_filter(l,SAMPLE_RATE,notch_freq_Hz),1,filtered)
    # bandpass filter
    filtered = np.apply_along_axis(lambda l:mne.filter.filter_data(l,SAMPLE_RATE,l_freq=bp_lowcut,h_freq=bp_highcut),1,filtered)
    return filtered

def filter_signal_mne_8chan(data,bp_lowcut_ecg=8,bp_highcut_ecg=20,bp_lowcut_eeg=5,bp_highcut_eeg=50):
    """
    Filters 2D array of singals dim: (nchan = 8) x (len_timeseries)

    Input:
    - data : 2D array of raw signals; channel 1 is ECG and channels 2,3,4,5,6,7,8 are EEG
    - bp_lowcut_ecg : unit Hz - frequencies below this are discarded for ECG channels
    - bp_highcut_ecg : unit Hz - frequencies above this are discarded for ECG channels
    - bp_lowcut_eeg : unit Hz - frequencies below this are discarded (EEG channels)
    - bp_highcut_eeg : unit Hz - frequencies above this are discarded (EEG channels)

    Output:
        2D array, filtered signals
    """

    notch_freq_Hz = [60.0, 120.0] # define frequencies to notch filter

    filtered = data
    # notch filter
    filtered =  np.apply_along_axis(lambda l:mne.filter.notch_filter(l,SAMPLE_RATE,notch_freq_Hz),1,filtered)
    
    # bandpass filter, different band for different types of data
    filtered_ecg = filtered[:1]
    filtered_eeg = filtered[1:]
    filtered_ecg = np.apply_along_axis(lambda l:mne.filter.filter_data(l,SAMPLE_RATE,l_freq=bp_lowcut_ecg,h_freq=bp_highcut_ecg),1,filtered_ecg)
    filtered_eeg = np.apply_along_axis(lambda l:mne.filter.filter_data(l,SAMPLE_RATE,l_freq=bp_lowcut_eeg,h_freq=bp_highcut_eeg),1,filtered_eeg)
    # recombine into 2D array and return
    return np.concatenate([filtered_ecg,filtered_eeg])

def epoch_data(data, window_length = 2,overlap=0.5):
        """
        Separates the data into equal sized windows

        Input:
            - data: data to seperate into windows
            - window_length: length of the window in seconds
            - overlap: overlap, float in [0,1), in percentage overlap of windows
            
        Output:
            an array of windows, each 

        """
        sample_rate = 250 # Hz
        array_epochs = []
        i = 0
        window_size_hz = int(window_length * sample_rate)
        overlap_size_hz = int(overlap * window_length * sample_rate)

        while(i  <= len(data)-window_size_hz ):
            array_epochs.append(data[i:i+ window_size_hz ])
            i = i + window_size_hz - overlap_size_hz # This is what the raw data looks like
        
#         if i is not len(data) - 1:
#         array_epochs.append(data[i:len(data)])
        
        return np.array(array_epochs) 

# takes an array of epochs (epoched data) -- the kind returned by
def plot_epoched(epoched,maxdisp=50):
    for n,i in enumerate(epoched):
        if n>=maxdisp:
            break
        plt.figure(figsize=(9,5))
        plt.plot(i)
        plt.show()
    return

def get_heartrate(npeaks, nsamples):
    """
    Convert the number of peaks in a number of samples to a heart rate (bpm)

    Input:
    - npeaks : number of peaks
    - nsamples : number of samples

    Output:
        heart rate in BPM
    """
    return int((float(npeaks) * 250 * 60) / float(nsamples))

if __name__ == "__main__":
    file_path = "../data/2021-05-27/01-5_guitar_OpenBCI-RAW-2021-05-27_20-56-18.txt"
    # load only the ECG signal i.e. channel 1
    raw_signal = load_ecg(file_path)
    print("The raw ECG signal looks like this \n")

    # plot the raw ECG signal
    plt.figure(figsize=(9,6))
    plt.plot(np.arange(len(raw_signal[20:-1000]))/SAMPLE_RATE,raw_signal[20:-1000])
    plt.title("raw signal")
    plt.xlabel("time in seconds")
    plt.ylabel("micro volts")
    plt.show()

    # filter the raw signal w/ default bandpass params for ECG
    filtered = np.squeeze(filter_signal_mne_uniform_band(np.array([raw_signal])))
    # display the filtered signal
    print("\nThe filtered signal looks like this \n")
    plt.figure(figsize=(9,6))
    plt.plot(filtered[100:])
    plt.title("filtered ECG signal")
    plt.xlabel("Time")
    plt.ylabel("micro volts")
    plt.show()

    # epoch the data
    win_len = 1.5 # length of windows / each epoch
    overlap = 0.3 # percent overlap of each window 
    print("\nEpoching the data into windows of length {} seconds with {} percent overlap".format(win_len,overlap*100))
    epochs = epoch_data(filtered,win_len,overlap)
    # display the epochs
    print("\nHere are the first 5 epochs")
    plot_epoched(epochs,maxdisp=5) 

    # display the butterworth-only filtered signal
    butter_data = filter_ecg(raw_signal)
    plt.figure(figsize=(9,6))
    plt.plot(butter_data)
    plt.title("butterworth-filtered signal")
    plt.xlabel("Time")
    plt.ylabel("micro volts")
    plt.show()

    butter_epochs = epoch_data(butter_data,win_len,overlap)
    # display the epochs
    print("\nHere are the first 5 epochs")
    plot_epoched(butter_epochs,maxdisp=5) 

    # plot the QRS-filtered data
    qrs_data = filter_qrs(raw_signal)
    plt.figure(figsize=(9,6))
    plt.plot(qrs_data)
    plt.title("filtered qrs complexes")
    plt.xlabel("Time")
    plt.ylabel("micro volts")
    plt.show()

    qrs_epochs = epoch_data(qrs_data,win_len,overlap)
    # display the epochs
    print("\nHere are the first 5 epochs")
    plot_epoched(qrs_epochs,maxdisp=5) 
