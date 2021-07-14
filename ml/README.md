


# Using hrv_extraction.py 

To start extracting the Spider DataSet and it's features into csv files:  
``` python 
spider = Spider_Data_Loader()
spider.runner()
```

If you want to work individually with for a single entry, start by loading it: 
``` python
signals, fields = wfdb.rdsamp('drive03', pn_dir='drivedb') #Loading Auto Stress Data for Driver 3 from Physionet
patient_data = pd.DataFrame(signals, columns=fields['sig_name'], dtype='float') #Store it into Dataframe
patient_data.dropna(inplace=True) #Clean data by removing nans
data = np.asarray(patient_data['ECG']) #Transform into numpy array 
sr = fields['fs'] #Isolate sample_rate for later processing
extractor = Feature_Extractor(data, sr, []) #Initialize Extractor
```
You can then either apply the extractor to each window manually: 
```python 
windows, n_windows = window(data, sr, windowsize=20, overlap=0, min_size=20, filter=True) #Apply a window function 
features = extractor.get_all_features(windows[0], n_windows[0]) #Get Features for first window 
print(features.shape)
```

Or you can pass the entire dataset and it will output a matrix of shape sample slices x features 
```python 
features = extractor.feature_matrix_from_whole_sample()
print(features.shape)
```

Lastly, you can use each of these function to also include y_values. 
First load the gsr data: 
```python 
gsr = patient_data['foot GSR']
```
Then you can apply to windows of both the ecg and gsr data 
```python
windows, n_windows = window(data, sr, windowsize=20, overlap=10, min_size=20, filter=True) #Apply a window function
gsr_windows, _ = window(gsr, sr, windowsize=20, overlap=10, min_size=20, filter=False)
features = extractor.get_all_features(windows[0], n_windows[0], gsr_windows[0])
```
Or using the entire sample 
```python
features = extractor.feature_matrix_from_whole_sample(gsr = gsr)
print(features.shape)
```

If you want to save all the extracted data in a csv
```python
features = extractor.feature_matrix_from_whole_sample(gsr = gsr, to_csv=True)
print(features.shape)
```