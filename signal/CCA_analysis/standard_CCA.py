import numpy as np
from sklearn.cross_decomposition import CCA
# from cca_zoo.models.rcca import CCA


def standard_cca(signal, sampling_rate, fund_frequency, num_harmonics, *args, **kwargs):
    pts, _ = np.shape(signal)
    reference_signal = np.zeros((pts, 2*num_harmonics)) # sin/cos waves as reference
    T = np.linspace(1.0, pts, pts)/sampling_rate
    for i in range(num_harmonics):
        reference_signal[:, 2*i] = np.transpose(np.sin(2*np.pi*fund_frequency*T))
        reference_signal[:, 2*i+1] = np.transpose(np.cos(2*np.pi*fund_frequency*T))
    cca = CCA(n_components=1)
    cca.fit(signal, reference_signal) # fit the collected signal with sin/cos waves
    signal_c, reference_signal_c = cca.transform(signal, reference_signal)
    corr = np.corrcoef(signal_c.T, reference_signal_c.T)
    # return corr[0, 1], cca.weights[0], cca.weights[1], reference_signal
    return corr[0, 1], cca.x_weights_, cca.y_weights_, reference_signal # return the weights and correlation
