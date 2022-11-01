import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import spectrogram

# S02_data = loadmat("cleaned_S02_typeC.mat", simplify_cells=True)['data']
# data = S02_data[3, :, 0, 12]
# print(data)

S02 = np.load('S02_template_augmented.npy', allow_pickle=True).item()
fig, axs = plt.subplots(31, 8, figsize=(80, 310))
for i in range(31):
    freq = round(5.85 + 0.16*i, 2)
    print(freq, i)
    signal = S02.get(float(freq)).astype(float)
    for j in range(8):
        f, t, Sxx = spectrogram(signal[:, j], fs=250)
        # f, t, Sxx = spectrogram(data, fs=250)
        axs[i, j].pcolormesh(t, f, Sxx, shading='gouraud')
        axs[i, j].set_ylabel('Frequency [Hz]')
        axs[i, j].set_xlabel('Time [sec]')
        axs[i, j].set_ylim([0, 20])
# plt.show()
fig.savefig("Template_Spectrogram_Augmented.png")

"""
S02 = np.load('S02_template_old.npy', allow_pickle=True).item()
freq = 5.85
signal = S02.get(float(freq)).astype(float)
print(signal[:, 0])
plt.specgram(signal[:, 0], NFFT=32, Fs=250, noverlap=16)
plt.ylim([0, 10])
plt.show()
"""
