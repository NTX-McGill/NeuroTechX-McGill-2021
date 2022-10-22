import matlab.engine
import matlab
import numpy as np
from scipy.io import loadmat
from scipy.signal import filtfilt, cheby1, savgol_filter


engine = matlab.engine.start_matlab()
data = loadmat('Sub08.mat')['data'] # (8, 1250, 31, x)
# data = loadmat('Sub02.mat')['data']
data = data.astype(float)
# print(data.shape)
"""
freq_list = [8.0 + i*0.25 for i in range(32)]
freq_list.remove(12)
"""
"""
freq_list = [6.0 + i*0.2 for i in range(31)]
"""
"""
freq_list = [5.1 + i*0.25 for i in range(31)]
"""
freq_list = [5.85 + i*0.16 for i in range(31)]
acc = []
pred = []
for test_i in range(6):
    test_index = test_i
    data_test = data[:, :, :, test_index]  # 10 blocks, 4 is from 3 weeks ago, 6 from 3 week: S02, 5
    template_index = [i for i in range(6)]
    template_index.remove(test_index)
    data_template = data[:, :, :, template_index]
    data_template = np.mean(data_template, axis=3)
    results = []
    predictions = []
    onset = 50
    latency = 35
    d_len = 4
    for tar in range(len(freq_list)):
        beta, alpha = cheby1(N=2, rp=1.0, Wn=[4.9 / 125.0, 51.6 / 125.0], btype='band', output='ba')
        signal = data_test[:, :, tar]
        signal = filtfilt(beta, alpha, signal[:, onset + latency:int(onset + latency + 250 * d_len)])
        signal = savgol_filter(signal, 5, 2, mode='nearest')
        signal = matlab.double(signal.T.tolist())
        # beta, alpha = cheby1(N=2, rp=0.3, Wn=[7/125.0, 90/125.0], btype='band', output='ba')
        rho_array = []
        for i in range(len(freq_list)):
            template = filtfilt(beta, alpha, data_template[:, :, i])[:, onset+latency:int(onset+latency+250*d_len)]
            template = savgol_filter(template, 5, 2, mode='nearest')
            template = matlab.double(template.T.tolist())
            # rho = engine.FBCCA_IT(signal, freq_list[i], 7.0, 88.0, 5.0, template, 1.0, 0.5, 5.0, 250.0, 2.0)
            rho = engine.FBCCA_IT(signal, freq_list[i], 4.9, 51.6, 4.0, template, 1.0, 0.0, 4.0, 250.0, 2.0)
            rho_array.append(rho)
        print(np.argmax(rho_array))
        predictions.append(np.argmax(rho_array))
        results.append(int(np.argmax(rho_array) == tar))
    print(np.sum(results)/len(results))
    acc.append(np.sum(results)/len(results))
    print(predictions)
    pred.append(predictions)
print(acc)
print(np.mean(acc), np.std(acc))
print(pred)
# data_template = engine.mean(matlab.double(data_template), 4)

