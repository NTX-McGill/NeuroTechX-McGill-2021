import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import heartpy as hp
import wfdb
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks
from feature_extractions import Feature_Extractor #get_features_matrix, 
from utils import window
from heartpy.analysis import calc_rr, calc_fd_measures 



signals, fields = wfdb.rdsamp('drive03', pn_dir='drivedb') #Loading Auto Stress Data for Driver 3 from Physionet
patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float') #Store it into Dataframe
patient_data.dropna(inplace=True) #Clean data by removing nans
data = np.asarray(patient_data['ECG']) #Transform into numpy array 
sr = fields['fs'] #Isolate sample_rate for later processing
windows, n_windows = window(data, sr, windowsize=20, overlap=0, min_size=20, filter=True) #Apply a window function 
extractor = Feature_Extractor(data, sr, []) #Initialize Extractor

#You can either apply the extractor to each window manually 
features = extractor.get_all_features(windows[0], n_windows[0]) #Get Features for first window 
print(features.shape)

#Or you can pass the entire dataset and it will output a matrix of shape sample slices x features 
features = extractor.feature_matrix_from_whole_sample()
print(features.shape)