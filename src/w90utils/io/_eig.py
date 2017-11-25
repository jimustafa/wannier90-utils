from __future__ import absolute_import, division, print_function

import numpy as np


__all__ = ['read_eig', 'write_eig', 'read_hamiltonian']


def read_eig(fname):
    """
    Read EIG file.

    Parameters
    ----------
    fname : str

    Returns
    -------
    eig : ndarray, shape (nkpts, nbnds, nproj)

    """
    raw_data = np.loadtxt(fname)

    band_indices = raw_data[:, 0].astype(int)
    kpoint_indices = raw_data[:, 1].astype(int)

    nbnds = np.max(band_indices)
    nkpts = np.max(kpoint_indices)

    eig = raw_data[:, 2]
    eig = eig.reshape((nkpts, nbnds))

    return eig


def write_eig(fname, eig):
    r"""
    Write :math:`E_{n\mathbf{k}}` to EIG file.

    Parameters
    ----------
    fname : eig
    eig : ndarray, shape (nkpts, nbnds)


    """
    nkpts, nbnds = eig.shape
    indices = np.mgrid[:nbnds, :nkpts].reshape((2, nkpts*nbnds), order='F')+1

    band_indices = indices[0]
    kpoint_indices = indices[1]

    eig = eig.flatten()

    data = np.column_stack((band_indices, kpoint_indices, eig))

    np.savetxt(fname, data, fmt='%5d%5d%18.12f')


def read_hamiltonian(fname):
    """
    Read EIG file and return k-dependent Hamiltonian matrix.

    Parameters
    ----------
    fname: str

    Returns
    -------
    Hk: ndarray, shape (nkpts, nbnds, nbnds)

    """
    eig = read_eig(fname)
    nkpts, nbnds = eig.shape

    Hk = np.zeros((nkpts, nbnds, nbnds))
    di = np.diag_indices(nbnds)
    for ikpt in range(nkpts):
        Hk[ikpt][di] = eig[ikpt]

    return Hk


read_hk = read_hamiltonian
