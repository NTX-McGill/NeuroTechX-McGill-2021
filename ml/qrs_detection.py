import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

import sys, os

sys.path.append('./ml/')

from hrv_extraction import Spider_Data_Loader

spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01')

data_length = int(ecg.shape[0] / sr)
FS = 250
og_sample_pts = np.arange(0, data_length, 1/sr)
new_sample_pts = np.arange(0, data_length, 1/FS)

upsampled_ecg = np.interp(new_sample_pts, og_sample_pts, ecg[:og_sample_pts.shape[0]])

order = 2
notch_freq = 60
nb, na = signal.iirnotch(notch_freq, Q=60, fs=FS)
notched_ecg = signal.lfilter(nb, na, upsampled_ecg)

lo, hi = 5, 15
lb, la = signal.butter(order, [lo,hi], btype='band', fs=FS)
filtered_ecg = signal.lfilter(lb, la, notched_ecg)

def ms_to_pts(ms, fs=250):
    return int(ms / 1000 * fs)

def LT(x, C=100, w=130):
    def _LTi(x, i, C, w_len):
        y = x[i-w_len: i]
        delta_y = y[1:] - y[:-1]

        return np.sum(np.sqrt(C + delta_y**2))

    w_len = ms_to_pts(w, fs=FS)
    _LTi_vect = np.vectorize(lambda i: _LTi(x, i, C, w_len))
    return _LTi_vect(np.arange(w_len, x.shape[0]))

LT_ecg = LT(filtered_ecg)

plt.plot(LT_ecg[5100:5200])

MIN_THRESH = 100 #Default min threshold value
EYE_CLOSE = 250 #Eye close period duration
NDP = 2.5 * 1000 #Adjust threshold if no QRS found in NDP seconds

base_threshold = 3 * np.mean(LT_ecg[:ms_to_pts(10, FS)])

def decision_rule(lt, i, T, fs=250):
    '''
    lt : LT transform of ECG signal
    i : current index of signal
    T : base threshold value for decision decision rule
    fs : signal sampling frequency

    Returns qrs_detected, [qrs_start, qrs_end], new_base_thresh
    '''

    actual_T = T / 3

    if lt[i] < actual_T:
        return False, [-1, -1], T

    Lmin = np.min(lt[i-ms_to_pts(125):i])
    Lmax = np.max(lt[i:i+ms])
