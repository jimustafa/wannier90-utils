from __future__ import absolute_import, division, print_function

import numpy as np


__all__ = ['read_kpoints', 'read_bands']


def read_kpoints(fname):
    raw_data = np.loadtxt(fname, skiprows=1)
    kpoints = raw_data[:, (0, 1, 2)]
    kweights = raw_data[:, 3]

    return kpoints


def read_bands(fname):
    nkpts = None
    with open(fname, 'r') as f:
        for iln, line in enumerate(f):
            if len(line.strip()) == 0:
                nkpts = iln
                break

    if nkpts is None:
        raise Exception

    raw_data = np.loadtxt(fname)
    nbnds = len(raw_data) // nkpts
    bands = raw_data[:, 1].reshape((nbnds, nkpts)).transpose()

    return bands
