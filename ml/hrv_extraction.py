import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import heartpy as hp
import wfdb
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks
from feature_extractions import get_features_matrix 

#Load data for driver 3 
signals, fields = wfdb.rdsamp('drive03', pn_dir='drivedb')
#Clean data 
patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float')
patient_data.dropna(inplace=True)
data = np.asarray(patient_data['ECG'])
#Download feature matrix 
fm = get_features_matrix(data, sr = fields['fs'] ) 
print(fm.shape)


