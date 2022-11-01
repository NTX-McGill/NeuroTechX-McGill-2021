# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 21:52:53 2022

@author: wsycx
"""

#from FBCCA_IT import filter_bank_cca_it
from scipy.io import loadmat
from scipy.signal import filtfilt, cheby1, butter, iirnotch
import argparse
import numpy as np
from standard_CCA import standard_cca
from standard_CCA_ITCCA import standard_cca_it_cca
from tqdm import tqdm
import matplotlib.pyplot as plt

#%% load dataset


'''
From README.txt

This dataset gathered SSVEP-BCI recordings of 35 healthy subjects 
(17 females, aged 17-34 years, mean age: 22 years) focusing on 40 
characters flickering at different frequencies (8-15.8 Hz with an
interval of 0.2 Hz). For each subject, the experiment consisted of
6 blocks. Each block contained 40 trials corresponding to all 40 
characters indicated in a random order. Each trial started with 
a visual cue (a red square) indicating a target stimulus. The cue 
appeared for 0.5 s on the screen. Subjects were asked to shift their 
gaze to the target as soon as possible within the cue duration. 
Following the cue offset, all stimuli started to flicker on the 
screen concurrently and lasted 5 s. After stimulus offset, the 
screen was blank for 0.5 s before the next trial began, which 
allowed the subjects to have short breaks between consecutive trials. 
Each trial lasted a total of 6 s. To facilitate visual fixation, 
a red triangle appeared below the flickering target during the stimulation 
period. In each block, subjects were asked to avoid eye blinks during the 
stimulation period. To avoid visual fatigue, there was a rest for several 
minutes between two consecutive blocks.

EEG data were acquired using a Synamps2 system (Neuroscan, Inc.) 
with a sampling rate of 1000 Hz. The amplifier frequency passband ranged 
from 0.15 Hz to 200 Hz. Sixty-four channels covered the whole scalp of the 
subject and were aligned according to the international 10-20 system. The 
ground was placed on midway between Fz and FPz. The reference was located 
on the vertex. Electrode impedances were kept below 10 KΩ. To remove the 
common power-line noise, a notch filter at 50 Hz was applied in data recording. 
Event triggers generated by the computer to the amplifier and recorded on an 
event channel synchronized to the EEG data. 

The continuous EEG data was segmented into 6 s epochs (500 ms pre-stimulus, 
5.5 s post-stimulus onset). The epochs were subsequently downsampled to 250 Hz. 
Thus each trial consisted of 1500 time points. Finally, these data were stored 
as double-precision floating-point values in MATLAB and were named as subject 
indices (i.e., S01.mat, …, S35.mat). For each file, the data loaded in MATLAB 
generate a 4-D matrix named ‘data’ with dimensions of [64, 1500, 40, 6]. The 
four dimensions indicate ‘Electrode index’, ‘Time points’, ‘Target index’, 
and ‘Block index’. The electrode positions were saved in a ‘64-channels.loc’ 
file. Six trials were available for each SSVEP frequency. Frequency and phase 
values for the 40 target indices were saved in a ‘Freq_Phase.mat’ file.

Information for all subjects was listed in a ‘Sub_info.txt’ file. For each subject, 
there are five factors including ‘Subject Index’, ‘Gender’, ‘Age’, ‘Handedness’, and ‘Group’. 
Subjects were divided into an ‘experienced’ group (eight subjects, S01-S08) and a ‘naive’ group 
(27 subjects, S09-S35) according to their experience in SSVEP-based BCIs.
'''


'''
The four dimensions indicate: 
0:      ‘Electrode index’
1:      ‘Time points’
3:      ‘Target index’(in this case 40 different charactors in each block)
4:      ‘Block index’ (in this case 6 blocks)
'''

import scipy.io
PATH = "benchmark_Data/"
data = scipy.io.loadmat(PATH + 's2.mat').get('data')


#%% changed version of filter_bank_cca_it from FBCCA_IT
def filter_bank_cca_it(signal, fund_freq, lower_freq, upper_freq,
                       num_harmonics, template, sampling_rate, data_cutoff, num_fb=4, fb_a=1, fb_b=0,
                       filter_order=2, rp=1, *args, **kwargs):
    sum = []
    nyq = 0.5 * sampling_rate
    low = lower_freq/nyq
    high = upper_freq/nyq
    band = [low, high]
    for i in range(1, num_fb+1):
        b, a = cheby1(N=filter_order, rp=rp, Wn=[(lower_freq*i-1)/nyq, (upper_freq+2)/nyq], btype='band', output='ba')
        filter_bank = filtfilt(b, a, signal.T).T
        #print(filter_bank.shape)
        filter_bank_data, _ = filter_bank.shape
        filter_bank = filter_bank[:filter_bank_data-data_cutoff,:]
        #print("---------------------------------------------in filter_bank_cca_it")
        #print(filter_bank.shape)
        #print(template.shape)
        rho = standard_cca_it_cca(filter_bank, sampling_rate=sampling_rate, fund_frequency=fund_freq*i,
                                  num_harmonics=num_harmonics, template=template)
        sum.append(rho**2 * (1/(np.power(i, fb_a))+fb_b))
    r = np.sum(sum)
    return r


#%%
'''
@TODO: reduce the amount of for loops it is computationally expensive
'''
def cross_validate_fbcca(data, channels, num_harmonics=5, data_length=1.5, includes_latency=1, data_cutoff = 10):
    _, _, num_targets, num_blocks = data.shape  # data is a 4D numpy array
    scores = np.zeros([1, num_blocks])
    results = np.zeros([1, 40])
    matrix = np.zeros([40, 40])

    for b in tqdm(range(num_blocks)):
        blocks = np.delete(np.arange(num_blocks), b) # blocks contains all blocks expect block b
        for j in range(num_targets):
            test = data[channels, 125+35*includes_latency:int(125+35*includes_latency+250*data_length), j, b].T
            unfilt = None
            for v in blocks:
                if unfilt is None:
                    unfilt = data[:, :, j, v]
                else:
                    unfilt += data[:, :, j, v]
            unfilt /= (num_blocks-1) # unfilt is the average of the rest of the blocks
            #print(unfilt.shape)
            unfilt = unfilt[channels, 125+35*includes_latency:int(125+35*includes_latency+250*data_length)] # take the 2 second segments
            #print(unfilt.shape)
            beta, alpha = cheby1(N=2, rp=1, Wn=[7/125.0, 90/125.0], btype='band', output='ba')
            template = filtfilt(beta, alpha, unfilt).T # filt with filtfilt function
            #print(template.shape)
            template_data, _ = template.shape
            template = template[:template_data-data_cutoff,:]
            #print(template.shape)
            for k in range(5):
                for i in range(8):
                    # taking 8-88 Hz signals 
                    rho = filter_bank_cca_it(signal=test, fund_freq=8+1*i+0.2*k, lower_freq=8,
                                             upper_freq=88, num_harmonics=num_harmonics,
                                             template=template, sampling_rate=250, data_cutoff = data_cutoff)
                    results[0, i+8*k] = rho
            matrix[j, :] = results
        counter = 0
        for i in range(num_targets):
            arg = np.argmax(matrix[i, :])
            if arg == i:
                counter += 1
        scores[0, b] = counter * 100.0 / num_targets
        #print(scores)
    return np.mean(scores, axis=1), np.std(scores, axis=1)


"""
test = np.transpose(data[:, :, 0, 0])
test_template = np.transpose(np.mean(data[:, :, 0, 1:5], axis=2))

corr, Wx, Wy, reference_signal = standard_cca(test, sampling_rate=250, fund_frequency=8, num_harmonics=4)
print(corr, Wx.shape, Wy.shape, reference_signal.shape)
print(standard_cca_it_cca(test, sampling_rate=250, fund_frequency=8, num_harmonics=4, template=test_template))
r = filter_bank_cca_it(test, fund_freq=8, lower_freq=7, upper_freq=88, num_harmonics=4,
                       template=test_template, sampling_rate=250)
print(r)
"""
def data_cutoff_exp(data,test_size):
    all_channels = [47, 53, 54, 55, 56, 57, 60, 61, 62]
    cutoff_size_list = [] 
    mean_list = []
    std_list = []
    for i in range(test_size):
        print("------------------- experiment " + str(i) + "---------------------")
        mean, std = cross_validate_fbcca(data=data, channels=all_channels, num_harmonics=5, data_length=2, data_cutoff=i*2)
        cutoff_size_list.append(i*5)
        mean_list.append(mean)
        std_list.append(std)
    return np.array(cutoff_size_list), np.array(mean_list), np.array(std_list)

#%% unit testing
#all_channels = [47, 53, 54, 55, 56, 57, 60, 61, 62]
#mean, std = cross_validate_fbcca(data=data, channels=all_channels, num_harmonics=5, data_length=2, data_cutoff=5)

#%% experiment 
from scipy.io import savemat
cutoff_size_array, mean_array, std_array = data_cutoff_exp(data,120)
#%%
cutoff_size_array = (cutoff_size_array/5)*2
PATH_result = "CCA_analysis/data_cutoff_experiment_result/experiment_dataCutOff_0_to_238/"
savemat(PATH_result+"cutoff_size_array.mat",{'cutoff_size_array':cutoff_size_array})
savemat(PATH_result+"mean_array.mat",{'mean_array':mean_array})
savemat(PATH_result+"std_array.mat",{'std_array':std_array})


#%%
plt.plot(cutoff_size_array,mean_array)
plt.title("correlation mean vs cutoff_size")
plt.xlabel("cutoff_size(points)")
plt.ylabel("mean corelation between template and test signal")
plt.show()