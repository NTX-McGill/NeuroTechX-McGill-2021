import numpy as np
from scipy.io import loadmat
from scipy.signal import filtfilt, cheby1, butter, iirnotch
import matplotlib.pyplot as plt


def build_template(mat_file_str, low_f=5.5, high_f=54.0):
    data = loadmat(mat_file_str, simplify_cells=True)['data']
    # print(np.shape(data))
    template = np.nanmean(data, axis=3)
    # print(np.shape(template))
    b, a = cheby1(N=2, rp=1, Wn=[low_f/125.0, high_f/125.0], btype='band', output='ba')
    template_dict = {
        freq: filtfilt(b, a, template[:, :, index]).T
        for index, freq in enumerate(np.around(np.arange(5.85, 10.651, 0.16), decimals=2))
    }

    np.save('S08_template.npy', template_dict)
    # plt.plot(template_dict.get(5.85+0.16*2)[:, 4])
    # plt.show()


if __name__ == '__main__':
    file_name = 'S08_typeC.mat'
    build_template(file_name)
    # data = np.load('S08_template.npy', allow_pickle=True)
    # print(data)
