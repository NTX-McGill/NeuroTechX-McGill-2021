from scipy.io import loadmat
from scipy.signal import filtfilt, cheby1, butter, iirnotch
import argparse
import numpy as np
from standard_CCA import standard_cca
from standard_CCA_ITCCA import standard_cca_it_cca
from FBCCA_IT import filter_bank_cca_it
import warnings


def cross_validate_fbcca(data, channels, num_harmonics=5, data_length=4.2, includes_latency=1):
    _, _, num_targets, num_blocks = data.shape  # data is a 4D numpy array
    scores = np.zeros([1, num_blocks])
    results = np.zeros([1, 40])
    matrix = np.zeros([40, 40])

    for b in range(num_blocks):
        blocks = np.delete(np.arange(num_blocks), b)
        for j in range(num_targets):
            test = data[channels, 125+35*includes_latency:int(125+35*includes_latency+250*data_length), j, b].T
            unfilt = None
            for v in blocks:
                if unfilt is None:
                    unfilt = data[:, :, j, v]
                else:
                    unfilt += data[:, :, j, v]
            unfilt /= (num_blocks-1)
            unfilt = unfilt[channels, 125+35*includes_latency:int(125+35*includes_latency+250*data_length)]

            beta, alpha = cheby1(N=2, rp=1, Wn=[7/125.0, 90/125.0], btype='band', output='ba')
            template = filtfilt(beta, alpha, unfilt).T
            for k in range(5):
                for i in range(8):
                    rho = filter_bank_cca_it(signal=test, fund_freq=8+1*i+0.2*k, lower_freq=8,
                                             upper_freq=88, num_harmonics=num_harmonics,
                                             template=template, sampling_rate=250)
                    results[0, i+8*k] = rho
            matrix[j, :] = results
        counter = 0
        for i in range(num_targets):
            arg = np.argmax(matrix[i, :])
            if arg == i:
                counter += 1
        scores[0, b] = counter * 100.0 / num_targets
        print(scores)
    return np.mean(scores, axis=1), np.std(scores, axis=1)


def main():
    warnings.filterwarnings(action='ignore')
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    data_path = args.file_path
    # assume the input is .mat file array, no header
    content = loadmat(data_path)
    data = np.array(content.get('data'))
    """
    test = np.transpose(data[:, :, 0, 0])
    test_template = np.transpose(np.mean(data[:, :, 0, 1:5], axis=2))
    
    corr, Wx, Wy, reference_signal = standard_cca(test, sampling_rate=250, fund_frequency=8, num_harmonics=4)
    print(corr, Wx.shape, Wy.shape, reference_signal.shape)
    print(standard_cca_it_cca(test, sampling_rate=250, fund_frequency=8, num_harmonics=4, template=test_template))
    r = filter_bank_cca_it(test, fund_freq=8, lower_freq=7, upper_freq=88, num_harmonics=4,
                           template=test_template, sampling_rate=250)
    print(r)
    """
    all_channels = [47, 53, 54, 55, 56, 57, 60, 61, 62] # 64 channels, index: 0-63
    # all_channels = [i for i in range(64)]
    mean, std = cross_validate_fbcca(data=data, channels=all_channels, num_harmonics=5, data_length=4.2)
    print(mean, std)
    mean, std = cross_validate_fbcca(data=data, channels=all_channels, num_harmonics=5, data_length=3.0)
    print(mean, std)
    """
    mean, std = cross_validate_fbcca(data=data, channels=all_channels, num_harmonics=5, data_length=1)
    print(mean, std)
    mean, std = cross_validate_fbcca(data=data, channels=all_channels, num_harmonics=5, data_length=0.5)
    print(mean, std)
    """


if __name__ == '__main__':
    main()
