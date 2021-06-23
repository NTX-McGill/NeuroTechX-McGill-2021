import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import heartpy as hp
import wfdb
from wfdb import processing
from heartpy.datautils import rolling_mean, _sliding_window
from heartpy.peakdetection import detect_peaks
import utils

#Load data from csv 
data = hp.get_data('e0103.csv')

#You can full service process the dataset into windowed dataset 
utils.make_windowed_dataset2(data, sample_rate=250, windowsize=20, overlap=0)

#Or you can extract peaks on your own generate features 
#METHOD 1: Heartpy
peaks = utils.calculate_peaks_heartpy(data, windowsize=.75, sample_rate=250)

#METHOD 2: WFDB
peaks = utils.calculate_peaks_wfdb(data, sample_rate = 250)