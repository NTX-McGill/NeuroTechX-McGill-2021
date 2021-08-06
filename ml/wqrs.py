from scipy import signal
from hrv_extraction import Spider_Data_Loader 
from utils import load_visualise, upsample
import heartpy as hp 
import matplotlib.pyplot as plt 
import numpy as np
from math import ceil, sqrt

'''
OPEN ISSUES: 
- How to decide on BUFLN?  

'''


def upsample(ecg, sr, fs=250): 
    data_length = int(ecg.shape[0] / sr)
    og_sample_pts = np.arange(0, data_length, 1/sr)
    new_sample_pts = np.arange(0, data_length, 1/fs)
    return np.interp(new_sample_pts, og_sample_pts, ecg[:og_sample_pts.shape[0]])

def sec_to_pts(s, fs=250):
    return int(s * fs)

def ltsamp(sig, t):  
    Yn = Yn1 = Yn2 = 0 
    ebuf, lbuf = np.array([np.sqrt(lfsc) for i in range(LTwindow+1)]),  np.zeros(LTwindow+1) #8192
    tt =  -1 
    aet = 0
    while(t > tt): 
        print(tt)
        Yn2 = Yn1 
        Yn1 = Yn
        v0, v1, v2 = sig[tt], sig[tt-LPn], sig[tt-LP2n]
        Yn = 2*Yn1 - Yn2 + v0 - 2*v1 + v2
        dy = (Yn-Yn1)/LP2n #Lowpass derivative of input 
        tt += 1
        et =  np.sqrt(lfsc + dy * dy)
        ebuf[tt] = et 
        # ebuf.append(et)
        aet += et - ebuf[tt-LTwindow]
        lbuf[tt] = aet 
        # lbuf.append(aet)
    return lbuf[t]

def LT2(sig, t, C = 1): 
    y = sig[t-LTwindow: t]
    delta_y = y[1:] - y[:-1]
    return np.sum(np.sqrt(C + delta_y**2))

def LT(x, C=1, w=.13):
    def _LTi(x, i, C, w_len):
        y = x[i-w_len: i]
        delta_y = y[1:] - y[:-1] / LP2n #added this scaling constant 
        return np.sum(np.sqrt(C + delta_y**2))

    w_len = sec_to_pts(w, fs=FS)
    _LTi_vect = np.vectorize(lambda i: _LTi(x, i, C, w_len))
    return _LTi_vect(np.arange(w_len, x.shape[0]))


def detect(sig, LT_func): 
    FROM = 0 
    to = len(sig)
    timer = 0 
    next_minute = FROM + spm 
    peaks = [] 
    
    print("***Calculating Initial Threshold***")
    t1 = FROM + sec_to_pts(8)

    #My Init Threshold    
    T0 = 0  
    for t in range(FROM, t1): 
        T0 += LT_func(sig, t)
    T0 /= t1 - FROM 
    Ta = 3 * T0 

    #MY other init threshold 
    # LT_vals = [] 
    # for t in range(FROM, t1): 
    #     LT_vals.append(LT2(sig, t))
    # T0 = np.mean(LT_vals)
    # Ta = T0 * 3
    
    #ROLAND's Init threshold 
    # LT_ecg = LT(sig, C=1, w=.13)
    # T02= np.mean(LT_ecg[FROM:t1]) 
    # Ta2 = T02 * 3
    
    # print("compare thresholds: mine: {}, R: {}".format(Ta, Ta2))
    # load_visualise(sig[FROM:t1], [Ta2 for i in range(t1-FROM)]) 
     
    print("***Initial Threshold Set to: {}".format(Ta)) 

    # Main loop 
    for t in range(FROM, to): 
        learning = 1
        if t % 250  == 0:  
            print('***Running Values for: {} sec / {}, learning: {}'.format(t/250, int(to-FROM)/250), learning)
        if learning: 
            if t > t1: 
                learning = 0 
                T1 = T0 
                t = FROM #start over 
            else: 
                T1 = 2*T0 
	    #Compare a length-transformed sample against T1.
        if (LT_func(sig, t) > T1): #Found possible QRS near t
            # print("***Potential QRS Found***")
            timer = 0 #Used for counting time after previous QRS 
            max = min = LT_func(sig, t) 
            # print("***Finding Max***")
            for tt in range(t+1,t + EyeClosing//2): 
                if LT_func(sig, tt) > max: max = LT_func(sig, tt) 
            # print("***Finding Min***")
            for tt in range(t-1, t - EyeClosing//2, -1): 
                if LT_func(sig, tt) < min: min = LT_func(sig, tt) 
            if (max > min+10): #There is a QRS near tt
                #Find QRS onset (PQ Junction)
                onset = max/100 + 2 
                tpq = t - 5 
                for tt in range(t, t-EyeClosing//2, -1): 
                    if (LT_func(sig, tt) - LT_func(sig, tt-1) < onset and 
                        LT_func(sig, tt-1) - LT_func(sig, tt-2) < onset and 
                        LT_func(sig, tt-2) - LT_func(sig, tt-3) < onset and 
                        LT_func(sig, tt-3) - LT_func(sig, tt-4) < onset): 
                        tpq = tt - LP2n # account for phase shift 
                        break 
                if (not learning): 
                    print("Peak found at : {}".format(t))
                    peaks.append(tpq) 
                #Adjust Thresholds 
                Ta += (max - Ta)/10 
                T1 = Ta/3 

                #Lock out further detections during eye closing period 
                t += EyeClosing
        elif (not learning): 
            #Once we get past the learning period, decrease threshold if no QRS was detected recently 
            timer += 1 
            if (timer > ExpectPeriod):
                Ta -= 1 
                T1 = Ta / 3 
        if (t >= next_minute): 
            next_minute += spm 
            print(".") 
    load_visualise(sig, peaks)

print("***Loading Data***")
spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01')

print("***Upsampling Data***")
upsampled_ecg = upsample(ecg, sr, fs=250)

print("***Init for Global Vars***")
FS = sps = 250 #Sampling Frequency 
# BUFLN = 16384 #must be a power of 2, see ltsamp() 
EYE_CLS = 0.25 #eye-closing period is set to 0.25 sec (250 ms)
MaxQRSw = 0.13 #maximum QRS width 0.13 sec (130ms)
NDP	 = 2.5 #adjust threshold if no QRS found in NDP seconds 
PWFreqDEF = 60 #power line (mains) frequency, in Hz (default)
TmDEF	=  100 #minimum threshold value (default)
# samplingInterval = 1000.0/sps  
lfsc = 1 # FIX THIS EVENTUALLY TO BE : 1.25*gain*gain/sps
spm = 60 * sps #samples per minute 
LPn = int(sps/PWFreqDEF); 	#The LP filter will have a notch at the power line (mains) frequency 
if (LPn > 8):  LPn = 8	# avoid filtering too agressively 
LP2n = int(2 * LPn)
EyeClosing = int(sps * EYE_CLS) # set eye-closing period (in samples)
ExpectPeriod = int(sps * NDP)	#maximum expected RR interval (in samples)
LTwindow = int(sps * MaxQRSw)  #length transform window size (in samples)


detect(upsampled_ecg[:10000], ltsamp)

# /******************************************************************************

#                             Online C Compiler.
#                 Code, Compile, Run and Debug C program online.
# Write your code in this editor and press "Run" button to compile and execute it.

# *******************************************************************************/

# #include <stdio.h>
# #define BUFLN 8
# #define LT 40
# #define LTwindow 2
# void print_array(char* name, int* ebuf){
#     printf("%s: ", name);
#     for(int i = 0; i < 10; i++) {
#             printf("%d, ", ebuf[i]);
#         } 
#     printf("\n");
# }
 
# int ltsample(t){
#     int *ebuf, *lbuf;
#     static int aet = 0, et; 
#     ebuf = (int * ) malloc ((unsigned) BUFLN * sizeof(int));
#     lbuf = (int * ) malloc ((unsigned) BUFLN * sizeof(int));
#     for (int i = 0; i<10; i++){
#         ebuf[i] = i;
#     } 
#     // print_array("lbuf before", lbuf);
#     int tt = -1L; 
#     while(t > tt){
#         printf("tt: %ld, t: %ld \n", tt, t);
#         print_array("ebuf", ebuf);
#         printf("VALUE1::: %d \n", (tt+1) & (BUFLN-1));
#         et = ebuf[(++tt) & (BUFLN-1)] = LT;
        
#         // printf("changing index number: %d \n", (++tt) & (BUFLN-1));
#         print_array("ebuf", ebuf);
#         printf("VALUE2:::: %d \n", (tt-LTwindow) &(BUFLN-1));
#         aet += et - ebuf[(tt-LTwindow) &(BUFLN-1)];
#         lbuf[(tt) & (BUFLN-1)] = aet; 
        
#         // lbuf[(tt) & (BUFLN-1)] = aet += et - ebuf[(tt-LTwindow) &(BUFLN-1)];
#         print_array("lbuf", lbuf);
#     }
#     printf("final index: %d", (t & BUFLN-1));
# }

# int main()
# {
#     printf("Hello World \n");
#     ltsample(3L);

#     return 0;
# }
