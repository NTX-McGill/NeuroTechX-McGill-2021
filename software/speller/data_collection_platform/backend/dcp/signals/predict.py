from FBCCA_IT import filter_bank_cca_it
import numpy as np
import json


def predict_letter(bci_data, subject_id='S08'):
    prediction = None
    # bci_data # 8 channels of x seconds data, sampling rate = 250Hz, then shape = (250x, 8)
    # parameters
    corr = []
    sampling_rate = 250.0
    low_bound_freq = 5.5
    upper_bound_freq = 54.0
    num_harmonics = 5  # parameter of FBCCA
    onset = 35  # remove visual latency
    # dummy = np.random.rand(500, 8)  # 8 channels of 2s data, sampling rate = 250Hz
    # Template for each subject is stored locally, will be loaded as matlab array (for convenience) before inference.
    # Could be implemented differently
    # template is basically averaged data previously collected given the same stimulus frequency
    template = np.load(f'{subject_id}_template.npy', allow_pickle=True).item()

    """
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

    with open("freq_letter_map.json") as fp:
        freq_letter_dict = json.load(fp)
    # print(freq_letter_dict)
    signal_len = np.shape(bci_data)[0]
    for frequency in list(freq_letter_dict.keys()):  # Do FBCCA for every frequency, find the one with max corr

        rho = filter_bank_cca_it(bci_data[onset:, :], float(frequency), low_bound_freq, upper_bound_freq, num_harmonics,
                                 template.get(float(frequency)).astype(float)[onset:signal_len+1, :], sampling_rate)
        corr.append(rho)
    prediction_index = np.argmax(corr)
    predicted_letter = freq_letter_dict.get(list(freq_letter_dict.keys())[prediction_index])

    return predicted_letter


if __name__ == '__main__':
    predict_letter(np.random.rand(1000, 8))
