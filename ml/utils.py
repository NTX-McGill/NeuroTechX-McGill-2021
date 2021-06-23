import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import heartpy as hp
import wfdb
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks, make_windows
from heartpy import process_segmentwise

def load_visualise(ecg, peaks, zoom_in=[]): 
    if zoom_in: #explore signal
        plt.figure(figsize=(12,3))
        plt.scatter(peaks, [ecg[int(x)] for x in peaks], color='red')
        plt.title("Filtering:{}, Zoom:{}".format(filter, zoom_in))
        plt.plot(ecg)
        plt.xlim(zoom_in[0], zoom_in[1])
        plt.show()
    else: 
        plt.figure(figsize=(12,3))
        plt.scatter(peaks, [ecg[int(x)] for x in peaks], color='red')
        plt.plot(ecg)
        plt.title("Filtering:{}, Zoom:{}".format(filter, zoom_in))
        plt.show()
    
    return ecg

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


