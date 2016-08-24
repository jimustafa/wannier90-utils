from __future__ import absolute_import, division, print_function

import numpy as np
from scipy.io import FortranFile


# __all__ = ['read_unk', 'write_unk']


# def read_unk(fname, gspace=False):
#     with FortranFile(fname) as f:
#         [ngx, ngy, ngz, ikpt, nbnds] = f.read_ints()

#         ngtot = ngx * ngy * ngz
#         unk_r = np.zeros((nbnds, ngtot), dtype=complex)
#         for ibnd in range(nbnds):
#             unk_r[ibnd, :] = f.read_reals().view(complex)

#     unk_r = unk_r.reshape((nbnds, ngx, ngy, ngz), order='F') / np.sqrt(ngtot)

#     if gspace:
#         unk_g = np.fft.fftn(unk_r, axes=(1, 2, 3)).reshape((nbnds, ngtot), order='F') / np.sqrt(ngtot)
#         return unk_g
#     else:
#         return unk_r


# def write_unk(fname, unk, ikpt):
#     (nbnds, ngx, ngy, ngz) = unk.shape

#     with FortranFile(fname, 'w') as f:
#         f.write_record(np.array([ngx, ngy, ngz, ikpt+1, nbnds], dtype=np.int32))

#         for ibnd in range(nbnds):
#             f.write_record(unk[ibnd].ravel(order='F').view(float))
