from FBCCA_IT import filter_bank_cca_it
from scipy.io import loadmat
from scipy.signal import filtfilt, cheby1, butter, iirnotch
import argparse
import numpy as np
from standard_CCA import standard_cca
from standard_CCA_ITCCA import standard_cca_it_cca
from FBCCA_IT import filter_bank_cca_it


def cross_validate_fbcca(data, channels, num_harmonics=5, data_length=1.5, includes_latency=1, *, N, r):  # forced
    _, _, num_targets, num_blocks = data.shape  # data is a 4D numpy array
    scores = np.zeros([1, num_blocks])
    results = np.zeros([1, 40])
    matrix = np.zeros([40, 40])

    for b in range(num_blocks):
        blocks = np.delete(np.arange(num_blocks), b)
        for j in range(num_targets):
            test = data[channels, 125 + 35 * includes_latency:int(125 + 35 * includes_latency + 250 * data_length), j,
                   b].T
            unfilt = None
            for v in blocks:
                if unfilt is None:
                    unfilt = data[:, :, j, v]
                else:
                    unfilt += data[:, :, j, v]
            unfilt /= (num_blocks - 1)
            unfilt = unfilt[channels, 125 + 35 * includes_latency:int(125 + 35 * includes_latency + 250 * data_length)]
            beta, alpha = cheby1(N=N, rp=r, Wn=[7 / 125.0, 90 / 125.0], btype='band', output='ba')
            template = filtfilt(beta, alpha, unfilt).T
            for k in range(5):
                for i in range(8):
                    rho = filter_bank_cca_it(signal=test, fund_freq=8 + 1 * i + 0.2 * k, lower_freq=8,
                                             upper_freq=88, num_harmonics=num_harmonics,
                                             template=template, sampling_rate=250)
                    results[0, i + 8 * k] = rho
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
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    data_path = args.file_path
    # assume the input is .mat file array, no header
    content = loadmat(data_path)
    data = np.array(content.get('data'))
    channels = [47, 53, 54, 55, 56, 57, 60, 61, 62]

    # ********************** grid search for filter order and ripple param **********************

    # ini vars
    pos = 0
    lin_space_order = np.linspace(2, 10, num=5)
    lin_space_rippl = np.linspace(1, 10, num=10)
    grid_params = np.meshgrid(lin_space_order, lin_space_rippl)
    mean_result = np.zeros((lin_space_rippl.shape[0] * lin_space_order.shape[0]))
    stds_result = np.zeros((lin_space_rippl.shape[0] * lin_space_order.shape[0]))

    for x in np.nditer(grid_params):
        mean, std = cross_validate_fbcca(data=data, channels=channels, num_harmonics=5, data_length=2, N=x[0], r=x[1])
        print(f'Filter-order {x[0]} & ripple {x[1]} ----> mean: {mean}, std: {std}')
        mean_result[pos], stds_result[pos] = mean, std
        pos += 1

    # np.reshape(mean_result, (10, 5))
    # np.reshape(stds_result, (10, 5))
    indices_max = (-mean_result).argsort()[:2]  # top 2
    print("*"*30)
    print(f'indices of max: {indices_max}')
    print(f'corresponding values: {mean_result[indices_max[0]]}, {mean_result[indices_max[1]]}')


if __name__ == '__main__':
    main()
