import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import heartpy as hp
import wfdb
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks
from feature_extractions import Feature_Extractor #get_features_matrix, 
import utils
# from utils import window, transform_y, load_visualise, calculate_peaks_wfdb, bandpass, RR_intervals
from heartpy.analysis import calc_rr, calc_fd_measures 
from scipy.signal import resample

def upsample(ecg, sr, new_sr = 250, gsr = None): 
    time = len(ecg)/sr/60 
    new_samp_num = new_sr * time * 60 
    resampled_data = resample(ecg, int(new_samp_num))
    return resampled_data

class Spider_Data_Loader: 
    def __init__(self):
        pass
    
    #Loading the spider data 
    def load_physiodata(self, instance, db = 'drivedb'): 
        signals, fields = wfdb.rdsamp(instance, pn_dir=db) #Loading Auto Stress Data for Driver 3 from Physionet
        patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float') #Store it into Dataframe
        patient_data.dropna(inplace=True) #Clean data by removing nans
        ecg = np.asarray(patient_data['ECG']) #Transform into numpy array 
        gsr = np.asarray(patient_data['foot GSR'])
        sr = fields['fs'] #Isolate sample_rate for later processing
        return ecg, gsr, sr
    
    def runner(self): 
        ppl = wfdb.io.get_record_list(db_dir = 'drivedb', records='all') #drivedb
        for p in ppl: 
            try: 
                print("LOADING DATA FOR", p)
                ecg, gsr, sr = self.load_physiodata(p)
                # print(sr)
                wd, m = hp.process(ecg, sample_rate = sr)
                peaks = wd['RR_list']
                data = utils.load_visualise(ecg, peaks)
                extractor = Feature_Extractor(ecg, sr, [], apply_bandpass=False) #Initialize Extractor
                features = extractor.feature_matrix_from_whole_sample(gsr = gsr, to_csv=p)
                print("LOADED DATA FOR", p, "SIZE", features.shape)
            except():
                print(p, "DIDNT WORK")


spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01')
# time = len(ecg)/sr/60 
# sr = len(ecg)/time/60
# samp_num = time * sr * 60 
# # print("sr:{}, time:{}, samp#:{}".format(sr, time, samp_num))
# new_sr = 250 
# new_samp_num = new_sr * time * 60  
# # print(len(ecg), samp_num, new_samp_num)
# resampled_data = resample(ecg, int(new_samp_num))
# print(len(resampled_data))


resampled_data = upsample(ecg, sr)

# peak_det = utils.Peak_Detection_Options() 
# peaks = peak_det.calculate_peaks_wfdb(resampled_data, 250)
# peaks = peak_det.RR_intervals(resampled_data, 250, 30)['RR_list']
# print(peaks)
# utils.load_visualise(resampled_data, peaks)
filtered = hp.filter_signal(resampled_data, cutoff = 0.05, sample_rate = 250, filtertype='notch')
scaled = hp.scale_data(filtered)
wd, m = hp.process(hp.scale_data(filtered), 250)
peaks = wd['peaklist']
# utils.load_visualise(ecg = scaled, peaks=[])

# hp.plot_poincare(wd, m)

# #visualise in plot of custom size
# plt.figure(figsize=(12,4))
# hp.plotter(wd, m)
# plt.show() 