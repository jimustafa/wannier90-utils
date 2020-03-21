import numpy as np


def unitarize(a):
    u, _, v = np.linalg.svd(a, full_matrices=False)
    return np.einsum('...ik,...kj->...ij', u, v)
