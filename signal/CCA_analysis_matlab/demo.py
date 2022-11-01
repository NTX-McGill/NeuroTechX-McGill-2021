import matlab.engine
import matlab
import numpy as np

eng = matlab.engine.start_matlab()  # start matlab engine in advance will speed things up.
freq_letter_dict = {  # mapping between frequency and letters
    8.0: 'A',
    8.25: 'B',
    8.5: 'C'
}
dummy = eng.rand(500, 8)       # 8 channels of 2s data, sampling rate = 250Hz
# Template for each subject is stored locally, will be loaded as matlab array (for convenience) before inference.
# Could be implemented differently
dummy_template = {  # template is basically averaged data previously collected given the same stimulus frequency
    8.0: eng.rand(500, 8),
    8.25: eng.rand(500, 8),
    8.5: eng.rand(500, 8)
}
""" For numpy array signal, convert to matlab before calling
dummy_np = np.random.rand(8. 500)
dummy = matlab.double(dummy_np.tolist())
"""
corr = []
sampling_rate = 250.0
filter_order = 2.0
a = 1.0  # parameter of FBCCA
b = 0.0  # parameter of FBCCA
num_fb = 4.0  # parameter of FBCCA
low_bound_freq = 8.0
upper_bound_freq = 88.0
num_harmonics = 4.0  # parameter of FBCCA
for frequency in list(freq_letter_dict.keys()):   # Do FBCCA for every frequency, find the one with max corr
    rho = eng.FBCCA_IT(dummy, frequency, low_bound_freq, upper_bound_freq, num_harmonics, dummy_template.get(frequency),
                       a, b, num_fb, sampling_rate, filter_order)
    corr.append(rho)
prediction = np.argmax(corr)
predicted_letter = freq_letter_dict.get(list(freq_letter_dict.keys())[prediction])
print(predicted_letter)
