import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#Python is wierd, have to manually add path to ML directory
import sys, os
sys.path.append('./ml/')

#Load data
from hrv_extraction import Spider_Data_Loader
spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01')

#Upsample data to not have a horrible sampling rate
data_length = int(ecg.shape[0] / sr)
FS = 250
og_sample_pts = np.arange(0, data_length, 1/sr)
new_sample_pts = np.arange(0, data_length, 1/FS)
upsampled_ecg = np.interp(new_sample_pts, og_sample_pts, ecg[:og_sample_pts.shape[0]])

#2nd order notch filter at 60Hz and 2nd order bandpass filter at [5,15] Hz range
order = 2
notch_freq = 60
nb, na = signal.iirnotch(notch_freq, Q=60, fs=FS)
notched_ecg = signal.lfilter(nb, na, upsampled_ecg)

lo, hi = 5, 15
lb, la = signal.butter(order, [lo,hi], btype='band', fs=FS)
filtered_ecg = signal.lfilter(lb, la, notched_ecg)

#The functions needed to run the main loop
def sec_to_pts(s, fs=250):
    return int(s * fs)

def LT(x, C=100, w=0.13):
    '''Computes the LT tranform of the entire time series'''

    def LTi(x, i, C, w_len):
        '''Computer the LT transform of the data at an index i'''
        y = x[i-w_len: i]
        dy = y[1:] - y[:-1]

        return np.sum(np.sqrt(C + dy**2))

    w_len = sec_to_pts(w, fs=FS)
    LTi_vect = np.vectorize(lambda i: LTi(x, i, C, w_len))
    return LTi_vect(np.arange(w_len, x.shape[0]))

LT_ecg = LT(filtered_ecg)

#Define constants for the main loop
MIN_T = 100 #Default min threshold value
EYE_CLOSE = 0.25 #Eye close period duration
NDP = 2.5 #Adjust threshold if no QRS found in NDP seconds
LP2n = 2 * FS // notch_freq #For phase shift? Not quite sure why this is used just keeping it for now since it's used in the OG algorithm

eye_closing = sec_to_pts(EYE_CLOSE, FS)
expect_period = sec_to_pts(NDP, FS)

FROM, TO = 0, len(LT_ecg)
LEARNING_PERIOD = 8
t1 = FROM + sec_to_pts(LEARNING_PERIOD)

learning_actual_T = np.mean(LT_ecg[FROM:t1]) #Setup base threshold and actual threshold values
base_T = 3 * learning_actual_T

qrs_detected = []
t = FROM
timer = 0
n_minutes = 1 #Keep track of how much time has passed
IS_LEARNING = True

#Main loop
while t < TO:
    #On first pass, learn what threshold to use - learning ends after 'LEARNING_PERIOD' seconds
    if IS_LEARNING:
        if t > t1:
            IS_LEARNING = False
            actual_T = learning_actual_T
            t = 0
            print('Learning done, starting over.')
        else:
            actual_T = learning_actual_T

    if LT_ecg[t] > actual_T: #Found a possible QRS near t
        timer = 0
        ltmax = np.max(LT_ecg[t+1: t + eye_closing//2])
        ltmin = np.min(LT_ecg[t - eye_closing//2 + 1 : t])

        '''This conditional is changed from original algorithm'''
        if (ltmax - ltmin) * 100000 > 13:
            onset = ltmax / 100 + 2
            tpq = t - 5

            #Search backwards for monotonic change near ltmin
            #Vectorize this part later
            for tt in range(t-1, t - eye_closing//2, -1):
                if (LT_ecg[tt]   - LT_ecg[tt-1] < onset and
                    LT_ecg[tt-1] - LT_ecg[tt-2] < onset and
                    LT_ecg[tt-2] - LT_ecg[tt-3] < onset and
                    LT_ecg[tt-3] - LT_ecg[tt-4] < onset):

                    tpq = tt - LP2n
                    break

            if not IS_LEARNING:
                qrs_detected.append(tpq)

        #Adjust thresholds
        base_T += (ltmax - base_T) / 10
        actual_T = base_T / 3

        #Lock out further detections during the eye-closing period
        t += eye_closing
    elif not IS_LEARNING:
        #Once past the learning period, decrease threhold if no QRS was recently detected
        timer += 1

        if timer > expect_period and base_T > MIN_T:
            base_T -= 1
            actual_T = base_T / 3

    t += 1

    #Track progress by printing how much time has passed
    if not IS_LEARNING and t // (FS * 60 * n_minutes) >= 1:
        print('{} minutes have passed'.format(n_minutes))
        n_minutes += 1
