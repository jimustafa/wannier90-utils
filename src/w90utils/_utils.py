from __future__ import absolute_import, division, print_function

import numpy as np


def unitarize(a):
    u, _, v = np.linalg.svd(a, full_matrices=False)
    return np.einsum('...ik,...kj->...ij', u, v)
