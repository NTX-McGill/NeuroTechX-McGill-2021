from scipy.signal import filtfilt, butter, cheby1
from sklearn.cross_decomposition import CCA
import numpy as np
from standard_CCA_ITCCA import standard_cca_it_cca


def filter_bank_cca_it(signal, fund_freq, lower_freq, upper_freq,
                       num_harmonics, template, sampling_rate, num_fb=5, fb_a=1, fb_b=0.3,
                       filter_order=2, rp=1, *args, **kwargs):
    sum = []
    nyq = 0.5 * sampling_rate
    low = lower_freq/nyq
    high = upper_freq/nyq
    band = [low, high]
    for i in range(1, num_fb+1):
        b, a = cheby1(N=filter_order, rp=rp, Wn=[(lower_freq*i-1)/nyq, (upper_freq+2)/nyq], btype='band', output='ba')
        filter_bank = filtfilt(b, a, signal.T).T
        rho = standard_cca_it_cca(filter_bank, sampling_rate=sampling_rate, fund_frequency=fund_freq*i,
                                  num_harmonics=num_harmonics, template=template)
        sum.append(rho**2 * (1/(np.power(i, fb_a))+fb_b))
    r = np.sum(sum)
    return r
