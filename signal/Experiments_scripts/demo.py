from FBCCA_IT import filter_bank_cca_it
import numpy as np


freq_letter_dict = {  # mapping between frequency and letters
    8.0: 'A',
    8.25: 'B',
    8.5: 'C'
}
dummy = np.random.rand(500, 8)       # 8 channels of 2s data, sampling rate = 250Hz
# Template for each subject is stored locally, will be loaded as matlab array (for convenience) before inference.
# Could be implemented differently
dummy_template = {  # template is basically averaged data previously collected given the same stimulus frequency
    8.0: np.random.rand(500, 8),
    8.25: np.random.rand(500, 8),
    8.5: np.random.rand(500, 8)
}
""" For numpy array signal, convert to matlab before calling
dummy_np = np.random.rand(8. 500)
dummy = matlab.double(dummy_np.tolist())
"""
corr = []
sampling_rate = 250.0
low_bound_freq = 8.0
upper_bound_freq = 88.0
num_harmonics = 4  # parameter of FBCCA
for frequency in list(freq_letter_dict.keys()):   # Do FBCCA for every frequency, find the one with max corr
    rho = filter_bank_cca_it(dummy, frequency, low_bound_freq, upper_bound_freq, num_harmonics,
                             dummy_template.get(frequency), sampling_rate)
    corr.append(rho)
prediction = np.argmax(corr)
predicted_letter = freq_letter_dict.get(list(freq_letter_dict.keys())[prediction])
print(predicted_letter)
