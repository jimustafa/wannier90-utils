from __future__ import absolute_import, division, print_function
import sys

import numpy as np


def read_kpoints(fname):
    raw_data = np.loadtxt(fname, skiprows=3)
    kpoints = raw_data[:, (1, 2, 3)]

    return kpoints


def write_kpoints(fname, kpoints):
    with open(fname, 'w') as f:
        print_kpoints(kpoints, file=f)


def print_kpoints(kpoints, header='', units='crystal', file=sys.stdout):
    print(header, file=file)
    print('%s' % units, file=file)
    print(len(kpoints), file=file)
    for (ik, kpt) in enumerate(kpoints):
        print('%5d%18.12f%18.12f%18.12f' % tuple([ik+1] + list(kpt)), file=file)


def read_bands_kpoints(fname):
    """
    Read k-points from the geninterp dat file

    Parameters
    ----------
    fname : str

    Returns
    -------
    kpoints : ndarray, shape (nkpts, 3)
        array of kpoints using for geninterp, in of units :math:`\frac{1}{\text{\AA}}`

    """
    raw_data = np.loadtxt(fname)

    nkpts = int(np.max(raw_data[:, 0]))
    nbnds = len(raw_data) // nkpts

    kpoints = raw_data[np.arange(0, len(raw_data), nbnds), 1:4]

    return kpoints


def read_bands(fname):
    raw_data = np.loadtxt(fname)
    nkpts = int(np.max(raw_data[:, 0]))
    bands = raw_data[:, 4]
    bands = bands.reshape((nkpts, -1))

    return bands


def read_band_velocities(fname):
    raw_data = np.loadtxt(fname)

    if not raw_data.shape[1] > 5:
        return None

    nkpts = int(raw_data[-1, 0])
    vnk = raw_data[:, 5:]
    vnk = vnk.reshape((nkpts, -1, 3))

    return vnk


read_vnk = read_band_velocities


def _read_boltzwann_data(fname):
    raw_data = np.loadtxt(fname)

    if raw_data.ndim == 1:
        nT = 1
        nmu = 1
        raw_data = raw_data.reshape((1, -1))
        mu, T = raw_data[:, (0, 1)].T
    else:
        mu, T = raw_data[:, (0, 1)].T

        dT = T[1] - T[0]
        nT = int(np.rint((np.max(T) - np.min(T))/dT))+1
        T = T[:nT]

        mu = mu.reshape((-1, nT))[:, :1]
        nmu = len(mu)

    raw_data = raw_data.reshape((nmu, nT, 8))

    data = {
        'xx': raw_data[:, :, 2],
        'xy': raw_data[:, :, 3],
        'yy': raw_data[:, :, 4],
        'xz': raw_data[:, :, 5],
        'yz': raw_data[:, :, 6],
        'zz': raw_data[:, :, 7],
    }

    return data, mu, T


def read_elcond(fname):
    return _read_boltzwann_data(fname)


def read_dos(fname):
    data = np.loadtxt(fname)
    e = data[:, 0]
    dos = data[:, 1]

    return e, dos
