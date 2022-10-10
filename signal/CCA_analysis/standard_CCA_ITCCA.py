import numpy as np
from standard_CCA import standard_cca
from IT_CCA import it_cca


def standard_cca_it_cca(signal, sampling_rate, fund_frequency, num_harmonics, template):
    corr1, Wxy, _, _ = standard_cca(signal, sampling_rate=sampling_rate, fund_frequency=fund_frequency,
                                    num_harmonics=num_harmonics)
    corr5, Wx, _ = it_cca(signal, template)
    corr2 = np.corrcoef(signal.dot(Wx).T, template.dot(Wx).T)
    corr3 = np.corrcoef(signal.dot(Wxy).T, template.dot(Wxy).T)
    _, Wxxy, _, _ = standard_cca(template, sampling_rate=sampling_rate, fund_frequency=fund_frequency,
                                 num_harmonics=num_harmonics)
    corr4 = np.corrcoef(signal.dot(Wxxy).T, template.dot(Wxxy).T)
    rho_array = np.array([corr1, corr2[0, 1], corr3[0, 1], corr4[0, 1], corr5])
    r = np.sum(np.sign(rho_array) * np.power(rho_array, 2))
    return r
