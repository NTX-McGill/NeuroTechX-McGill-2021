import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import heartpy as hp
import wfdb
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks
from feature_extractions import Feature_Extractor #get_features_matrix, 

from utils import window, transform_y, load_visualise, calculate_peaks_wfdb, bandpass, RR_intervals
from heartpy.analysis import calc_rr, calc_fd_measures 
from scipy.signal import resample


<<<<<<< HEAD
def load_physiodata(instance, db, x_name='ECG', y_name = 'foot GSR'): 
=======

def load_physiodata(instance, db): 
>>>>>>> 5060a3988792f1ee02a08d7ce890790d14fc1346
    signals, fields = wfdb.rdsamp(instance, pn_dir=db) #Loading Auto Stress Data for Driver 3 from Physionet
    patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float') #Store it into Dataframe
    patient_data.dropna(inplace=True) #Clean data by removing nans
    ecg = np.asarray(patient_data[x_name]) #Transform into numpy array 
    gsr = np.asarray(patient_data[y_name])
    sr = fields['fs'] #Isolate sample_rate for later processing
    return ecg, gsr, sr
    

# ecg, gsr, sr = load_physiodata('drive01', 'drivedb')
# wd, m = hp.process(ecg[60000:65000], sr)
# peaks = [ecg[i] for i in wd['peaklist']]
# load_visualise(ecg, [])

# patient_data = pd.read_csv('/Users/Owner/Desktop/School/NT/e0103.csv')
# patient_data.dropna(inplace=True)
# ecg = np.asarray(patient_data).flatten() 
# wd, m = RR_intervals(ecg.flatten(), sr, 30)
# print(wd['peaklist'])
# load_visualise(ecg, wd['peaklist'])

# peaks = calculate_peaks_wfdb(ecg, sr)

# ##Convert Entire dataset to collection of CSVs
# ppl = wfdb.io.get_record_list(db_dir = 'drivedb', records='all') #drivedb
# for p in ppl: 
#     try: 
#         print("LOADING DATA FOR", p)
#         ecg, gsr, sr = load_physiodata(p)
#         # print(sr)
#         wd, m = hp.process(ecg, sample_rate = sr)
#         peaks = wd['RR_list']
#         data = load_visualise(ecg, peaks)
#     #     extractor = Feature_Extractor(ecg, sr, [], apply_bandpass=False) #Initialize Extractor
#     #     features = extractor.feature_matrix_from_whole_sample(gsr = gsr, to_csv=p)
#     #     print("LOADED DATA FOR", p, "SIZE", features.shape)
    # except():
    #     print(p, "DIDNT WORK")

signals, fields = wfdb.rdsamp('drive03', pn_dir='drivedb') #Loading Auto Stress Data for Driver 3 from Physionet
patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float') #Store it into Dataframe
patient_data.dropna(inplace=True) #Clean data by removing nans
data = np.asarray(patient_data['ECG']) #Transform into numpy array 
sr = fields['fs'] #Isolate sample_rate for later processing
extractor = Feature_Extractor(data, sr, []) #Initialize Extractor


# #You can either apply the extractor to each window manually 
windows, n_windows = window(data, sr, windowsize=20, overlap=0, min_size=20, filter=True) #Apply a window function 
features = extractor.get_all_features(windows[0], n_windows[0]) #Get Features for first window 
print(features.shape)

# #Or you can pass the entire dataset and it will output a matrix of shape sample slices x features 
# features = extractor.feature_matrix_from_whole_sample()
# print(features.shape)

#Lastly, you can use each of these function to also include y_values
# gsr = patient_data['foot GSR']

# #Window by window
# windows, n_windows = window(data, sr, windowsize=20, overlap=10, min_size=20, filter=True) #Apply a window function
# gsr_windows, _ = window(gsr, sr, windowsize=20, overlap=10, min_size=20, filter=False)
# features = extractor.get_all_features(windows[0], n_windows[0], gsr_windows[0])

# #Or using the entire sample 
# features = extractor.feature_matrix_from_whole_sample(gsr = gsr)
# print(features.shape)

#If you want to save all the extracted data in a csv
# features = extractor.feature_matrix_from_whole_sample(gsr = gsr, to_csv=True)
# print(features.shape)
