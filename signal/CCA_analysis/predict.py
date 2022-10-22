from .standard_CCA import standard_cca
from .FBCCA_IT import filter_bank_cca_it
import numpy as np
import json
from scipy.signal import filtfilt, cheby1, iirnotch


def predict_letter(bci_data, subject_id='S02'):
    prediction = None
    # bci_data # 8 channels of x seconds data, sampling rate = 250Hz, then shape = (250x, 8)
    # parameters
    corr = []
    sampling_rate = 250.0
    low_bound_freq = 7.75 # lowest freq - + 0.25
    # low_bound_freq = 9.0
    upper_bound_freq = 16.25
    # upper_bound_freq = 12.0
    num_harmonics = 1  # parameter of FBCCA
    channels = [4]
    # channels = [0 , 1, 2, 3, 4, 5, 6, 7]  # index of channels used in prediction
    # onset = 80  # remove visual latency and head
    # notch_freq = 60
    # notch_Q = 10
    nyq_freq = sampling_rate / 2


    """ Generate freq_letter_map.json
    with open("keyboard_config.json") as fp:
        keyboard_dict = json.load(fp)
    freq_letter_dict = {
        float(v_dict['frequency']): k for k, v_dict in sorted(keyboard_dict.items())
    }
    freq_letter_dict = {k: v for k,v in sorted(freq_letter_dict.items())}
    with open("freq_letter_map.json", 'w') as outfile:
        json.dump(freq_letter_dict, outfile)
    return 
    """

    with open("./dcp/signals/freq_letter_map.json") as fp:
        freq_letter_dict = json.load(fp)
    # print(freq_letter_dict)
    signal_len = np.shape(bci_data)[0]
    # signal_len = 800
    # preprocessing: DC offset removal, notch filter, bandpass filter
    # only needs to be done once
    bci_data -= np.nanmean(bci_data, axis=0)
    # beta_notch, alpha_notch = iirnotch(notch_freq, notch_Q, fs=sampling_rate)
    # bci_data = filtfilt(beta_notch, alpha_notch, bci_data, axis=0)
    beta, alpha = cheby1(N=2, rp=0.3, Wn=[low_bound_freq / nyq_freq, upper_bound_freq / nyq_freq], btype='band', output='ba')
    bci_data = filtfilt(beta, alpha, bci_data.T).T

    for frequency in list(freq_letter_dict.keys()):  # Do FBCCA for every frequency, find the one with max corr
        bci_data_short = bci_data
        rho, _, _, _ = standard_cca(bci_data_short[:, channels], sampling_rate, float(frequency), num_harmonics)
        corr.append(rho)
    prediction_index = np.argmax(corr)
    predicted_letter = freq_letter_dict.get(list(freq_letter_dict.keys())[prediction_index])

    return predicted_letter


if __name__ == '__main__':
    predict_letter(np.random.rand(1000, 8))