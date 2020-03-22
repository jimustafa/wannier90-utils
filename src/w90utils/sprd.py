"""Functions for computing components of the spread"""

import numpy as np


def wannier_centers(m, bvectors, bweights):
    (nkpts, nntot, nwann) = m.shape[:-1]

    mii = m.reshape((nkpts*nntot, nwann, nwann)).diagonal(offset=0, axis1=1, axis2=2)

    bvectors = np.reshape(bvectors, (-1, 3))
    bweights = np.tile(bweights, nkpts)

    bwv = bweights[:, np.newaxis] * bvectors

    # Eq. 31
    rv = np.zeros((nwann, 3))
    for i in range(nwann):
        rv[i] = -1 * np.sum(bwv * np.imag(np.log(mii[:, i]))[:, np.newaxis], axis=0)
    rv /= nkpts

    return rv


def omega_d(m, bvectors, bweights, idx=None):   # Eq. 36
    """
    Compute the diagonal contribution to the spread functional

    Parameters
    ----------
    m: ndarray, shape (nkpts, nntot, nbnds, nbnds)
        the overlap matrix
    bvectors: ndarray, shape (nkpts, nntot, 3)
    bweights: ndarray, shape (nntot,)

    """
    (nkpts, nntot, nwann) = m.shape[:-1]

    rv = wannier_centers(m, bvectors, bweights)

    mii = np.copy(m.reshape((nkpts*nntot, nwann, nwann)).diagonal(offset=0, axis1=1, axis2=2))

    bvectors = np.reshape(bvectors, (-1, 3))
    bweights = np.tile(bweights, nkpts)

    bvrv = np.einsum('bi,ri->br', bvectors, rv)

    if idx is not None:
        sprd_d = np.sum(bweights[:, np.newaxis] * (-1 * np.imag(np.log(mii)) - bvrv)**2, axis=0) / nkpts
        sprd_d = sprd_d[idx]
    else:
        sprd_d = np.sum(bweights[:, np.newaxis] * (-1 * np.imag(np.log(mii)) - bvrv)**2) / nkpts

    return sprd_d


def omega_od(Mmn, bweights):            # Eq. 35
    """
    Compute the off-diagonal contribution to the spread functional

    Parameters
    ----------
    Mmn: ndarray, shape (nkpts, nntot, nbnds, nbnds)
        the overlap matrix
    bweights: ndarray, shape (nntot,)

    """
    (nkpts, nntot, nbnds) = Mmn.shape[:-1]

    m = Mmn.reshape((nkpts*nntot, nbnds, nbnds))
    mii = m.diagonal(offset=0, axis1=1, axis2=2)

    bweights = np.tile(bweights, nkpts)

    sprd_od = np.sum(bweights[:, np.newaxis, np.newaxis] * np.abs(m)**2)
    sprd_od -= np.sum(bweights[:, np.newaxis] * np.abs(mii)**2)
    sprd_od /= nkpts

    return sprd_od


def omega_dod(Mmn, bvectors, bweights):
    """
    Compute the sum of the diagonal and off-diagonal contribution to the spread
    functional

    Parameters
    ----------
    Mmn: ndarray, shape (nkpts, nntot, nbnds, nbnds)
        the overlap matrix
    bvectors: ndarray, shape (nkpts, nntot, 3)
    bweights: ndarray, shape (nntot,)

    """
    sprd_d = omega_d(Mmn, bvectors, bweights)
    sprd_od = omega_od(Mmn, bweights)

    return sprd_d + sprd_od


def omega_iod(m, bweights, idx=None):                # Eq. 43
    """
    Compute the sum of the invariant and off-diagonal contribution to the spread
    functional

    Parameters
    ----------
    m: ndarray, shape (nkpts, nntot, nbnds, nbnds)
        the overlap matrix
    bweights: ndarray, shape (nntot,)

    """
    (nkpts, nntot, nwann) = m.shape[:-1]

    mii = m.reshape((nkpts*nntot, nwann, nwann)).diagonal(offset=0, axis1=1, axis2=2)

    bweights = np.tile(bweights, nkpts)

    if idx is not None:
        sprd_iod = np.sum(bweights[:, np.newaxis] * (1 - np.abs(mii)**2), axis=0) / nkpts
        sprd_iod = sprd_iod[idx]
    else:
        sprd_iod = np.sum(bweights[:, np.newaxis] * (1 - np.abs(mii)**2)) / nkpts

    return sprd_iod


def omega_i(Mmn, bweights):
    """
    Compute the invariant contribution to the spread functional

    Parameters
    ----------
    Mmn: ndarray, shape (nkpts, nntot, nbnds, nbnds)
        the overlap matrix
    bweights: ndarray, shape (nntot,)

    """
    sprd_od = omega_od(Mmn, bweights)
    sprd_iod = omega_iod(Mmn, bweights)

    return sprd_iod - sprd_od


def omega(Mmn, bvectors, bweights):
    """
    Compute the spread functional

    Parameters
    ----------
    Mmn: ndarray, shape (nkpts, nntot, nbnds, nbnds)
        the overlap matrix
    bvectors: ndarray, shape (nkpts, nntot, 3)
    bweights: ndarray, shape (nntot,)

    """
    sprd_d = omega_d(Mmn, bvectors, bweights)
    sprd_iod = omega_iod(Mmn, bweights)

    return sprd_d + sprd_iod
