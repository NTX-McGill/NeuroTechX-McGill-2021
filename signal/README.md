# Siggy

### Code
``example_code/`` contains a jupyter notebook ``numpy and mne filtering examples.ipynb`` that shows you how to filter signals with mne library. There is also a numpy implementation but it doesn't seem to be doing a good job - someone will have to fix this. Also contains ``plot_all_spectrograms.py``: some informative code from 2019.

Note: it's bad form to push jupyter notebooks, should we move this to google colab along with the 2019 data?. 

``filter.py``, this filters ECG data. The code here can be built upon so that it filters all channels of data. 

``featurize.py``, requires ``filter.py``, filters signals and extracts featurse from them for ML to play with

``signal.py`` is a class for processing our *offline* data: ECG and EEG signals, contains methods from ``filter.py`` and ``featurize.py``. Keep this file tidy and well organized, the first time you implement an algorithm don't do it in here, test it somewhere else beforehand.

### Todo
- [ ] Make class for processed signals, for nicer code, more readable code
- [ ] Improve ``filter.py`` so that it filters EEG as well as ECG -- watch out we will probably need to use a different frequency band for the EEG signals than the 8Hz to 20Hz band we use for ECG
- [ ] Research: Look into what the mne and mne-realtime libraries have to offer, we may not have to code everything ourselves if we can make use of these efficiently.
- [ ] Start featurizing:
    - [ ] Implement peak detection algorithm
    - [ ] basic HRV (heart-rate variability) feature (keep in mind we'll have to make this a real-time feature, think about this when you design it)
    - [ ] Pointcare plots for nice visual display of HRV
    - [ ] Frequency domain HRV stuff
    - [ ] Look into wavelet transforms - maybe this is not great because our ECG data isn't so clean  
    - [ ] Spectrograms can be fed into computer vision algorithms, research + think of ways we could implement spectrograms 
