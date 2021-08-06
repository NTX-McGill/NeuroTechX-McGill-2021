from hrv_extraction import Spider_Data_Loader 
from utils import load_visualise, upsample
import heartpy as hp 
import matplotlib.pyplot as plt 
import numpy as np 

def upsample(ecg): 
    data_length = int(ecg.shape[0] / sr)
    og_sample_pts = np.arange(0, data_length, 1/sr)
    new_sample_pts = np.arange(0, data_length, 1/FS)
    return np.interp(new_sample_pts, og_sample_pts, ecg[:og_sample_pts.shape[0]])

def sec_to_pts(s, fs=250):
    return int(s * fs)

def ltsamp(sig, t, LPn, LP2n, lfsc, LTwindow):  
    Yn = Yn1 = Yn2 = 0 
    print(int(LTwindow))
    ebuf, lbuf = np.array([np.sqrt(lfsc) for i in range(int(LTwindow))]), np.zeros(int(LTwindow)) 
    tt =  -1 
    aet = 0
    
    while(t > tt): 
        # print("tt: {}, t: {}".format(tt, t))
        # print("ebuf: {}, lbuf: {}".format(ebuf, lbuf))
        # print("tt: {}, tt-LPn: {}, LP2n:{} ".format(tt, tt-LPn, tt-LP2n))
        v0, v1, v2 = sig[tt], sig[int(tt-LPn)], sig[int(tt-LP2n)]
        Yn = 2*Yn1 - Yn2 + v0 - 2*v1 + v2
        dy = (Yn-Yn1)/LP2n #Lowpass derivative of input 
        tt += 1
        et =  np.sqrt(lfsc + dy * dy)
        # print("VALUE1: {} of ebuf".format(tt))
        ebuf[tt] = et 
        aet += et - ebuf[int(tt-LTwindow)]
        # print("VALUE2: {} of lbuf".format(tt-LTWindow))
        lbuf[tt] = aet 
        print("ebuf: {}, lbuf: {}".format(ebuf, lbuf))
    return lbuf[-1]

def detect(sig, sr): 
    print("***Setting Global Vars***")
    sps = sr
    FROM = 0 
    to = len(sig)
    next_minute = FROM + spm 
    
    v = ltsamp(sig, 0, LPn, LP2n, lfsc, LTwindow)
    print(v)
    exit() 

    print("***Calculating Average***")
    t1 = FROM + sec_to_pts(8)   
    T0 = 0 
    for t in range(FROM, t1): 
        print("LOADING INFO FOR SAMPLE: {}".format(t))
        T0 += ltsamp(sig, t, LPn, LP2n, lfsc, LTwindow)
    T0 /= t1 - FROM 
    Ta = 3 * T0 

     

    # Main loop 
    for t in range(FROM, to): 
        print('***Running Values for Time: {}'.format(t))
        learning = 1
        if learning: 
            if t > t1: 
                learning = 0 
                T1 = T0 
                t = FROM #start over 
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


#Define Global Variables 
FS = 250 #Sampling Frequency 
BUFLN = 16384 #must be a power of 2, see ltsamp() 
EYE_CLS = 0.25 #eye-closing period is set to 0.25 sec (250 ms)
MaxQRSw = 0.13 #maximum QRS width (130ms)
NDP	 = 2.5 #adjust threshold if no QRS found in NDP seconds 
PWFreqDEF = 60 #power line (mains) frequency, in Hz (default)
TmDEF	=  100 #minimum threshold value (default)


print("***Loading Data***")
spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01')
# print("***Loaded Data***")

print("***Upsampling Data***")
upsampled_ecg = upsample(ecg)

sps = sr
samplingInterval = 1000.0/sps  
lfsc = 1 # FIX THIS EVENTUALLY TO BE : 1.25*gain*gain/sps
spm = 60 * sps
LPn = sps/PWFreqDEF; 	#The LP filter will have a notch at the power line (mains) frequency 
if (LPn > 8):  LPn = 8	# avoid filtering too agressively 
LP2n = 2 * LPn
EyeClosing = sps * EYE_CLS # set eye-closing period */
ExpectPeriod = sps * NDP	#maximum expected RR interval */
LTwindow = sps * MaxQRSw  #length transform window size */

detect(upsampled_ecg, 250)

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
