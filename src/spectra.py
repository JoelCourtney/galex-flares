import query.sdss
import numpy as np
import math
from pyraf import iraf
from iraf import noao, imred, ccdred


mu = [
    np.matrix([[0.55], [0.32]]),
    np.matrix([[0.78], [0.43]]),
    np.matrix([[0.95], [0.52]]),
    np.matrix([[1.15], [0.62]]),
    np.matrix([[1.41], [0.76]]),
    np.matrix([[1.87], [1.03]]),
    np.matrix([[2.09], [1.14]]),
    np.matrix([[2.49], [1.35]])
]

sigma = [
    np.matrix([[0.0159, 0.0039], [0.0039, 0.0083]]),
    np.matrix([[0.0135, 0.0051], [0.0051, 0.0055]]),
    np.matrix([[0.0163, 0.0061], [0.0061, 0.0058]]),
    np.matrix([[0.0204, 0.0076], [0.0076, 0.0076]]),
    np.matrix([[0.0213, 0.0086], [0.0086, 0.0085]]),
    np.matrix([[0.0183, 0.0084], [0.0084, 0.0062]]),
    np.matrix([[0.0194, 0.0072], [0.0072, 0.0054]]),
    np.matrix([[0.0270, 0.0107], [0.0107, 0.0095]])
]


def get_sdss_spectral_type(sourceID):
    sdss = query.sdss.get_sdss(sourceID)
    x = np.matrix([[sdss['r']-sdss['i']], [sdss['i']-sdss['z']]])
    return [(1./(2.*math.pi*math.sqrt(np.linalg.norm(sigma[i])))) * math.exp((-1./2)*np.transpose(x-mu[i])*np.linalg.inv(sigma[i])*(x-mu[i])) for i in range(8)]


def pyraf_test():
    iraf.imexamine("XMMLSS_MOS01-07.0051b.fits")


if __name__ == '__main__':
    # print(get_sdss_spectral_type('COSMOS_MOS22-09'))
    pyraf_test()