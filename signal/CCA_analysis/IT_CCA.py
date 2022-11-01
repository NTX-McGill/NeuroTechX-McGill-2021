import numpy as np
from sklearn.cross_decomposition import CCA
# from cca_zoo.models.rcca import CCA


def it_cca(signal, template):
    cca = CCA(n_components=1)
    cca.fit(signal, template)
    signal_c, template_c = cca.transform(signal, template)
    corr = np.corrcoef(signal_c.T, template_c.T)
    # return corr[0, 1], cca.weights[0], cca.weights[1]
    return corr[0, 1], cca.x_weights_, cca.y_weights_
