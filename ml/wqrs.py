from hrv_extraction import Spider_Data_Loader 
from utils import load_visualise, upsample
import heartpy as hp 
import matplotlib.pyplot as plt 
import numpy as np 

##DONT FORGET TO PAD WITH 0 at start  

# spider = Spider_Data_Loader()
# ecg, gsr, sr = spider.load_physiodata('drive01')

# n_signal = np.array([0, 1,7,5])
# s2 = n_signal[1:] - n_signal[:-1]

# print(s2)

def LT(signal, w, i, sr): 
    L = 0 
    for k in range(i-w, i): 
        C = 0 #1/sr
        delta_y = np.power(signal[k] - signal[k-1], 2)
        print(delta_y)
        L += np.sqrt(C + delta_y)
    return L 

def LT2(signal, w, i, C): 
    wind = signal[i-w:i+1]
    delta_y = np.power(wind - np.flip(wind), 2)
    print(delta_y)
    L = np.sum(delta_y + [C for i in range(len(wind))]) 
    return L 

# print(np.flip(n_signal))

# print(LT(n_signal, 3, 3, 0), LT2(n_signal, 3,3,0)) 

# upsampled = upsample(ecg, 15.5)
# wd, m = hp.process(upsampled[:300], 250) 
# peaks = wd['peaklist']
# load_visualise(upsampled[:300], peaks)



#Define Global Variables 

BUFLN = 16384 #must be a power of 2, see ltsamp() 
EYE_CLS = 0.25 #eye-closing period is set to 0.25 sec (250 ms)
MaxQRSw = 0.13 #maximum QRS width (130ms)
NDP	 = 2.5 #adjust threshold if no QRS found in NDP seconds 
PWFreqDEF = 60 #power line (mains) frequency, in Hz (default)
TmDEF	=  100 #minimum threshold value (default)

# sig = -1 


# /* ltsamp() returns a sample of the length transform of the input at time t.
#    Since this program analyzes only one signal, ltsamp() does not have an
#    input argument for specifying a signal number; rather, it always filters
#    and returns samples from the signal designated by the global variable
#    'sig'.  The caller must never "rewind" by more than BUFLN samples (the
#    length of ltsamp()'s buffers). */

def ltsamp(sig, t, LPn, LP2n, lfsc, LTwindow): 
    # BUFLN , LTWindow = 8, 2 
    Yn = Yn1 = Yn2 = 0 
    ebuf, lbuf = np.array([i for i in range(BUFLN)]), np.zeros(BUFLN)
    tt =  -1 
    aet = 0
    # print("lbuf before", lbuf)
    while(t > tt): 
        # print("tt: {}, t: {}".format(tt, t))
        # print("ebuf: {}, lbuf: {}".format(ebuf, lbuf))
        print("tt: {}, tt-LPn: {}, LP2n:{} ".format(tt, tt-LPn, tt-LP2n))
        v0, v1, v2 = sig[tt], sig[int(tt-LPn)], sig[int(tt-LP2n)]
        Yn = 2*Yn1 - Yn2 + v0 - 2*v1 + v2
        dy = (Yn-Yn1)/LP2n #Lowpass derivative of input 
        tt += 1
        et =  40 #np.sqrt(lfsc + dy * dy)
        # print("VALUE1: {} of ebuf".format(tt))
        ebuf[tt] = et 
        aet += et - ebuf[int(tt-LTwindow)]
        # print("VALUE2: {} of lbuf".format(tt-LTWindow))
        lbuf[tt] = aet 
        # print("ebuf: {}, lbuf: {}".format(ebuf, lbuf))
    return lbuf[-1]

def main(record, sr): 
    print("***Setting Global Vars***")
    sps = sr
    samplingInterval = 1000.0/sps
    pname = record  
    lfsc = 1 # FIX THIS EVENTUALLY TO BE : 1.25*gain*gain/sps
    spm = 60 * sps
    LPn = sps/PWFreqDEF; 	#The LP filter will have a notch at the power line (mains) frequency 
    if (LPn > 8):  LPn = 8	# avoid filtering too agressively 
    LP2n = 2 * LPn
    EyeClosing = sps * EYE_CLS # set eye-closing period */
    ExpectPeriod = sps * NDP	#maximum expected RR interval */
    LTwindow = sps * MaxQRSw  #length transform window size */
    from_ = 0 
    to = len(record)
    next_minute = from_ + spm
    peaks = [] 
    sig = record 

    '''/* Average the first 8 seconds of the length-transformed samples
       to determine the initial thresholds Ta and T0. The number of samples
       in the average is limited to half of the ltsamp buffer if the sampling
       frequency exceeds about 2 KHz. */'''
    print("***Calculating Average***")
    t1 = 8 + from_    
    T0 = 0 
    for t in range(from_, 8): 
        T0 += ltsamp(sig, t, LPn, LP2n, lfsc, LTwindow)
    T0 /= t1 - from_ 
    Ta = 3 * T0 
    # Main loop 
    for t in range(from_, to): 
        print('***Running Values for Time: {}'.format(t))
        learning = 1
        if learning: 
            if t > t1: 
                learning = 0 
                T1 = T0 
                t = from_ #start over 
            else: 
                T1 = 2*T0 
	    #Compare a length-transformed sample against T1.
        if (ltsamp(sig, t, LPn, LP2n, lfsc, LTwindow) > T1): #Found possible QRS near t
            timer = 0 #Used for counting time after previous QRS 
            max = min = ltsamp(sig, t, LPn, LP2n, lfsc, LTwindow)
            for tt in range(t+1,t + EyeClosing/2): 
                if (ltsamp(sig, tt, LPn, LP2n, lfsc, LTwindow) > max): max = ltsamp(tt)
            for tt in range(t-1, t - EyeClosing/2, -1): 
                if (ltsamp(sig, tt, LPn, LP2n, lfsc, LTwindow) < min): min = ltsamp(tt)
            if (max > min+10): #There is a QRS near tt
                #Find QRS onset (PQ Junction)
                onset = max/100 + 2 
                tpq = t - 5 
                for tt in range(t, t-EyeClosing/2, -1): 
                    if (ltsamp(sig, tt, LPn, LP2n, lfsc, LTwindow) - ltsamp(sig, tt-1, LPn, LP2n, lfsc, LTwindow) < onset and 
                        ltsamp(sig, tt-1, LPn, LP2n, lfsc, LTwindow) - ltsamp(sig, tt-2, LPn, LP2n, lfsc, LTwindow) < onset and 
                        ltsamp(sig, tt-2, LPn, LP2n, lfsc, LTwindow) - ltsamp(sig, tt-3, LPn, LP2n, lfsc, LTwindow) < onset and 
                        ltsamp(sig, tt-3, LPn, LP2n, lfsc, LTwindow) - ltsamp(sig, tt-4, LPn, LP2n, lfsc, LTwindow) < onset): 
                        tpq = tt - LP2n # account for phase shift 
                        break 
                if (not learning): 
                    peaks = tpq
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


print("***Loading Data***")
spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01')
# print("***Loaded Data***")

print("***Upsampling Data***")
data_length = int(ecg.shape[0] / sr)
FS = 250
og_sample_pts = np.arange(0, data_length, 1/sr)
new_sample_pts = np.arange(0, data_length, 1/FS)
upsampled_ecg = np.interp(new_sample_pts, og_sample_pts, ecg[:og_sample_pts.shape[0]])
# print("***Upsampled Data***")

main(upsampled_ecg, 250)





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
#}
