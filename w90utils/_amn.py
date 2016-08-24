from __future__ import absolute_import, division, print_function

import numpy as np


def expand_amn(a, kpoints, idx, Rvectors, nproj_atom=None):
    """
    Expand the projections matrix by translations of the orbitals

    Parameters
    ----------
    a : ndarray, shape (nkpts, nbnds, nproj)
    kpoints : ndarray, shape (nkpts, 3)
    idx : ndarray
        indices of translated orbitals
    Rvectors: ndarray
        translation vectors for the orbitals
    nproj_atom: ndarray, optional
        number of projections on each atom, with idx and Rvectors now describing
        atoms instead of orbitals

    """
    assert len(Rvectors) == len(idx)

    if nproj_atom is not None:
        assert len(nproj_atom) == len(idx)
        idx_new = []
        Rvectors_new = []
        for iatom, i in enumerate(idx):
            offset = np.sum(nproj_atom[:i])
            for j in range(nproj_atom[i]):
                idx_new.append(offset+j)
                Rvectors_new.append(Rvectors[iatom])

        idx = idx_new
        Rvectors = Rvectors_new

    nkpts, nbnds, nproj = a.shape

    a1 = np.zeros((nkpts, nbnds, len(idx)), dtype=complex)

    k_dot_R = np.einsum('ki,ri->kr', kpoints, Rvectors)
    exp_factors = np.exp(-1j * 2*np.pi * k_dot_R)

    a1 = a[:, :, idx] * exp_factors[:, np.newaxis, :]

    return a1
