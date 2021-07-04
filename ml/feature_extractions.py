import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import wfdb
from scipy import signal 
from wfdb import processing
from heartpy.datautils import get_samplerate_datetime, rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks, make_windows, check_peaks, fit_peaks
from heartpy import process_segmentwise
from heartpy.analysis import calc_rr, calc_fd_measures 
import heartpy as hp
from utils import window 


# # Features 

# """
# Notch and butteroworth bandpass 
# Need: NFD, NSD, HRV, (+)avNN, (+) sdNN, (+)rmSSD, NN50, (+)pNN50, (+)pNN20

# Already have from the processing tools
# 3?,8,9,10,11,12 

# """

# # Should we gonna forget about HR Nmean ? 

# # Mean of abs of normalized first differences
# def get_nfd(n_signal): # (4)
#     # takes normalized signal window --> returns feature 
#     diffs = abs(n_signal[:-1] - n_signal[1:])
#     return diffs.mean() 

# # mean of abs values of normed second differences
# def get_nsd(n_signal): # (5)
#     # normalized signal window --> feature
#     second_diffs = abs(n_signal[:-2] - n_signal[2:])
#     return second_diffs.mean() 

# # HRV, get the nn_intervals / window from "process segmentwise"
# def get_hrv(nn_intervals): # (6)
#     # takes list of nn_intervals (i.e. rr_intervals) [the intervals not the peaks!]
#     # Returns the heart rate variability (HRV)
#     return (nn_intervals[:-1] - nn_intervals[1:]).mean() 

# # Average normal to normal intervals
# def get_avNN(nn_intervals): # (7)
#     return nn_intervals.mean() 

# def get_sdNN(nn_intervals, avNN): # (8)
#     return np.sqrt(((nn_intervals - avNN)**2).mean()) 
    
# def get_rMSSD(nn_intervals): # (9)
#     return np.sqrt(((nn_intervals[1:] - nn_intervals[:-1])**2).mean())

# # Don't use feature (10) because it's stupid
# """
# This function at the bottom gets all the features we need about a window
# """

# FEAT_NAMES = ["nfd", "nsd", "hrv", "avNN", "sdNN", "rMSSD", "pNN20", "pNN50"]

# def get_all_features(win, n_win, sr):
#     """
#     :param window np.ndarray: 1d array, 2 second filtered window of data
#     :param n_window np.ndarray: 1d array, 2 second normalized window
#     """
#     # process data using the utils and extract relevant features automatically
#     wd, m = hp.process(win, sample_rate = sr)
#     rr_intervals = wd['RR_list'] / 4
#     # there are ready made features stored in m 
#     pNN20, pNN50 = m['pnn20'] , m['pnn50']

#     # extract some features
#     # Note : rr_intervals === nn_intervals
#     nfd, nsd, hrv, avNN = get_nfd(n_win), get_nsd(n_win), get_hrv(rr_intervals),get_avNN(rr_intervals) # 4, 5, 6, 7
#     sdNN = get_sdNN(rr_intervals, avNN) # 8
#     rMSSD = get_rMSSD(rr_intervals) # 9 


#     features = [nfd, nsd, hrv, avNN, sdNN, rMSSD, pNN20, pNN50]
#     return np.array(features)

# def get_features_matrix(data, sr):
#     windows, n_windows = window(data, sr, windowsize=10, overlap=0, min_size=0, filter=True) 
#     features_mat = []
#     for win,n_win in zip(windows,n_windows):
#         features_mat.append(get_all_features(win, n_win, sr)) 
#     return np.array(features_mat)



class Feature_Extractor(): 
    def __init__(self, data, sample_rate, feat_list, window_size = 20, overlap = 0, apply_bandpass = True) : 
        self.data = data 
        self.sr = sample_rate
        self.wsize= window_size
        self.ovrlp = overlap
        self.apply_bandpass = apply_bandpass
        self.feat_list = feat_list
        self.rr_intervals = None 
        self.nn_intervals = None

    def get_nfd(self, n_signal): # (4)
        # takes normalized signal window --> returns feature 
        diffs = abs(n_signal[:-1] - n_signal[1:])
        return diffs.mean() 

    # mean of abs values of normed second differences
    def get_nsd(self, n_signal): # (5)
        # normalized signal window --> feature
        second_diffs = abs(n_signal[:-2] - n_signal[2:])
        return second_diffs.mean() 

    # HRV, get the nn_intervals / window from "process segmentwise"
    def get_hrv(self, nn_intervals): # (6)
        # takes list of nn_intervals (i.e. rr_intervals) [the intervals not the peaks!]
        # Returns the heart rate variability (HRV)
        return (nn_intervals[:-1] - nn_intervals[1:]).mean() 

    # Average normal to normal intervals
    def get_avNN(self, nn_intervals): # (7)
        return nn_intervals.mean() 

    def get_sdNN(self, nn_intervals, avNN): # (8)
        return np.sqrt(((nn_intervals - avNN)**2).mean()) 
        
    def get_rMSSD(self, nn_intervals): # (9)
        return np.sqrt(((nn_intervals[1:] - nn_intervals[:-1])**2).mean())

    def get_all_features(self, win, n_win, gsr = None):
        """
        :param window np.ndarray: 1d array, 2 second filtered window of data
        :param n_window np.ndarray: 1d array, 2 second normalized window
        """
        # process data using the utils and extract relevant features automatically

        #extracting time domain features: pnn20, pnn50, nfd, nsd, hrv, avNN, sdNN, rMSSD
        wd, m = hp.process(win, sample_rate = self.sr)
        rr_intervals = wd['RR_list'] / 4
        pNN20, pNN50 = m['pnn20'] , m['pnn50']
        nfd, nsd, hrv, avNN = self.get_nfd(n_win), self.get_nsd(n_win), self.get_hrv(rr_intervals),self.get_avNN(rr_intervals) # 4, 5, 6, 7
        sdNN = self.get_sdNN(rr_intervals, avNN) # 8
        rMSSD = self.get_rMSSD(rr_intervals) # 9 
        # print("TIME DOMAIN FEATURES EXTRACTED")

        #extracting frequency domain features: vlf, lf, hf, lf_hf 
        wd, m = calc_fd_measures(method = 'periodogram', welch_wsize=self.wsize, measures = m, working_data = wd) #240
        vlf, lf, hf, lf_hf = m["vlf"], m["lf"], m["hf"], m["lf/hf"] 
        # print("FREQ DOMAIN FEATURES EXTRACTED")
    
        features = [nfd, nsd, hrv, avNN, sdNN, rMSSD, pNN20, pNN50, vlf, lf, hf, lf_hf]
        if gsr.any(): features.append(gsr.mean())
        
        
        return np.array(features)

    def feature_matrix_from_whole_sample(self, gsr=None, to_bin = False, to_csv=False): 
        windows, n_windows = window(self.data, self.sr, windowsize=self.wsize, overlap=0, min_size=0, filter=self.apply_bandpass)
        features_mat = []
        feat_names = ['nfd', 'nsd', 'hrv', 'avNN', 'sdNN', 'rMSSD', 'pNN20', 'pNN50', 'vlf', 'lf', 'hf', 'lf_hf']
        if gsr.any(): 
            print('gsr included')
            feat_names.append('foot GSR')
            gsr_windows, _ = window(gsr, self.sr, windowsize=self.wsize, overlap=0, min_size=0, filter=False)
            for i in range(len(windows)): 
                ecg, n_ecg, gsr = windows[i], n_windows[i], gsr_windows[i]
                features_mat.append(self.get_all_features(win = ecg, n_win = n_ecg, gsr=gsr)) 
        else: 
            for win,n_win in zip(windows,n_windows):
                features_mat.append(self.get_all_features(win, n_win))  
        if to_bin: 
            np.save('Feature_Extraction.npy', features_mat)
        if to_csv: 
            df = pd.DataFrame(features_mat, columns=feat_names)
            df.to_csv('Feature_Extraction.csv')
            # np.savetxt('Feature_Extraction.csv', features_mat)
        return np.array(features_mat)
    
    
