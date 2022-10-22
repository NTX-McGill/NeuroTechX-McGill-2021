import numpy as np
from scipy.io import loadmat
from scipy.signal import filtfilt, cheby1, butter, iirnotch
import matplotlib.pyplot as plt


def build_template(mat_file_str, low_f=5.5, high_f=22.0):
    data = loadmat(mat_file_str, simplify_cells=True)['data']
    # print(np.shape(data))
    template = np.nanmean(data, axis=3)
    # print(np.shape(template))
    b, a = cheby1(N=2, rp=1, Wn=[low_f/125.0, high_f/125.0], btype='band', output='ba')
    t = np.linspace(0, 5, 1250)
    template_dict = {
        freq: (filtfilt(b, a, template[:, :, index]).T + (np.reshape(5*np.sin(2*np.pi*freq*t), (1250, 1)) @ np.ones((1, 8)))
               + (np.reshape(1*np.sin(2*np.pi*freq*2*t), (1250, 1)) @ np.ones((1, 8))))
        for index, freq in enumerate(np.around(np.arange(5.85, 10.651, 0.16), decimals=2))
    }

    np.save('S02_template_augmented.npy', template_dict)
    # print(template_dict)

    # print(template_dict.get(round(5.85+0.16*4, 2)))
    plt.plot(template_dict.get(round(5.85+0.16*5, 2))[:, 0])
    plt.ylim([-20, 20])
    plt.show()


if __name__ == '__main__':
    file_name = 'channel_cleaned_S02_typeC.mat'
    build_template(file_name)
    # data = np.load('S08_template.npy', allow_pickle=True)
    # print(data)
