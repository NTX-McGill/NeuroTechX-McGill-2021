import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import wfdb
from scipy import signal 
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks, make_windows, check_peaks, fit_peaks
from heartpy import process_segmentwise
from heartpy.analysis import calc_rr
import heartpy as hp


def calculate_peaks_heartpy(data, windowsize, sample_rate, ma_perc = 20): 
    rol_mean = rolling_mean(data, windowsize, sample_rate)
    wd = detect_peaks(data, rol_mean, ma_perc, sample_rate)
    return(wd['peaklist'])
    
def calculate_peaks_wfdb(data, sample_rate): 
    xqrs = processing.XQRS(sig=data, fs=sample_rate)
    xqrs.detect()
    peaks = xqrs.qrs_inds 
    return peaks 

def make_windowed_dataset(data, sample_rate, windowsize=120, overlap=0, min_size=20, to_csv=False): 
    window_inds = make_windows(data, sample_rate, windowsize, overlap, min_size)
    windowed_data = np.array([data[i[0]: i[1]] for i in window_inds])
    if to_csv: 
        np.savetxt("windowed_e0103.csv", windowed_data, delimiter=",")
    return windowed_data

def make_windowed_dataset2(data, sample_rate, segment_width, segment_overlap, ): 
    wd, m  = process_segmentwise(data, sample_rate, segment_width, segment_overlap, segment_min_size=20, replace_outliers=False, outlier_method='iqr', mode='full')
    print(wd,m) 

def normalize_signal(signal):
    return (signal - signal.mean()) / signal.std()  

def bandpass_filter(data, sample_rate, min_size): 
    filtered = hp.filter_signal(data, cutoff=[5, 12], sample_rate=sample_rate, order=3, filtertype='bandpass')
    return filtered 
# filter and window (& normalize) data 
def window(data, sample_rate, windowsize, overlap, min_size, filter=True): 
    """
    :param data:
    :param overlap float: number in [0.0, 1.0) the proportion of overlap between windows

    """
    if filter: 
        data = bandpass_filter(data, sample_rate, min_size)
    window_inds = make_windows(data, sample_rate, windowsize, overlap, min_size)
    n_filtered = normalize_signal(data) # normalized and filtered
    windowed_data = np.array([data[i[0]: i[1]] for i in window_inds])
    n_windowed_data = np.array([n_filtered[i[0] : i[1]] for i in window_inds])
    return windowed_data , n_windowed_data 

def RR_intervals(data, sample_rate, windowsize = .75, ma_perc = 20, bpmmin=40, bpmmax=180): 
    
    working_data = {}
    bl_val = np.percentile(data, 0.1)
    if bl_val < 0:
        print('scaling data by absolute value')
        data = data + abs(bl_val)

    working_data['hr'] = data
    working_data['sample_rate'] = sample_rate

    rol_mean = rolling_mean(data, windowsize, sample_rate)

    peaks = fit_peaks(data, rol_mean, sample_rate, bpmmin=bpmmin,
                             bpmmax=bpmmax, working_data=working_data) 
    
    working_data = calc_rr(working_data['peaklist'], sample_rate, working_data=working_data)

    working_data = check_peaks(working_data['RR_list'], working_data['peaklist'], working_data['ybeat'],
                               False, working_data=working_data)

    return working_data

def clean_nans(df): 
    # df = df.replace([np.inf, -np.inf], np.nan)
    # df[~np.isfinite(df)] = np.nan
    df.dropna(inplace=True)
    return df

def load_visualise(ecg, peaks, zoom=[]):
    if zoom: #explore signal
        plt.figure(figsize=(12,3))
        plt.scatter(peaks, [ecg[int(x)] for x in peaks], color='red')
        plt.title("Filtering:{}, Zoom:{}".format(filter, zoom))
        plt.plot(ecg)
        plt.xlim(zoom[0], zoom[1])
        plt.show()
    else: 
    #and zoom in
        plt.figure(figsize=(12,3))
        plt.scatter(peaks, [ecg[int(x)] for x in peaks], color='red')
        plt.plot(ecg)
        plt.title("Filtering:{}, Zoom:{}".format(filter, zoom))
        plt.show()
    
    return ecg


