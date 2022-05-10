import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt


def build_template(mat_file_str):
    data = loadmat(mat_file_str, simplify_cells=True)['data']
    # print(np.shape(data))
    template = np.nanmean(data, axis=3)
    # print(np.shape(template))
    template_dict = {
        freq: template[:, :, index].T for index, freq in enumerate(np.around(np.arange(5.85, 10.651, 0.16), decimals=2))
    }

    np.save('S08_template.npy', template_dict)
    # plt.plot(template_dict.get(5.85+0.16*2)[4, :])
    # plt.show()


if __name__ == '__main__':
    file_name = 'S08_typeC.mat'
    build_template(file_name)
    data = np.load('S08_template.npy', allow_pickle=True)
    print(data)
