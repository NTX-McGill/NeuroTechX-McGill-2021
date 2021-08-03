


# Using hrv_extraction.py 

1. If you just want to load the data: 
``` python 
spider = Spider_Data_Loader()
ecg, gsr, sr = spider.load_physiodata('drive01') #this gives you data from one driver (1/17) 
```

2. To run the full service (load Spider DataSet and extract it's features then load into csv files):  
``` python 
spider = Spider_Data_Loader()
spider.runner()
```

3. If you want to work on feature extraction individually with for a single entry, you can either load it as above (1) or manually loading it like this : 
``` python
signals, fields = wfdb.rdsamp('drive03', pn_dir='drivedb') #Loading Auto Stress Data for Driver 3 from Physionet
patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float') #Store it into Dataframe
patient_data.dropna(inplace=True) #Clean data by removing nans
data = np.asarray(patient_data['ECG']) #Transform into numpy array 
sr = fields['fs'] #Isolate sample_rate for later processing
extractor = Feature_Extractor(data, sr, []) #Initialize Extractor
```
4. You can then either apply the extractor to each window manually: 
```python 
windows, n_windows = window(data, sr, windowsize=20, overlap=0, min_size=20, filter=True) #Apply a window function 
features = extractor.get_all_features(windows[0], n_windows[0]) #Get Features for first window 
print(features.shape)
```

5. Or you can pass the entire dataset and it will output a matrix of shape sample slices x features 
```python 
features = extractor.feature_matrix_from_whole_sample()
print(features.shape)
```

6. Lastly, you can use each of these function to also include y_values. 
First load the gsr data: 
```python 
gsr = patient_data['foot GSR']
```
7. Then you can apply to windows of both the ecg and gsr data 
```python
windows, n_windows = window(data, sr, windowsize=20, overlap=10, min_size=20, filter=True) #Apply a window function
gsr_windows, _ = window(gsr, sr, windowsize=20, overlap=10, min_size=20, filter=False)
features = extractor.get_all_features(windows[0], n_windows[0], gsr_windows[0])
```
8. Or using the entire sample 
```python
features = extractor.feature_matrix_from_whole_sample(gsr = gsr)
print(features.shape)
```

9. If you want to save all the extracted data in a csv
```python
features = extractor.feature_matrix_from_whole_sample(gsr = gsr, to_csv=True)
print(features.shape)
```
