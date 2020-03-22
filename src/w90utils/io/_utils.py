import numpy as np
from scipy.constants import codata
from functools import reduce


# energy conversions
Ha2eV = codata.value('Hartree energy in eV')
eV2Ha = 1/Ha2eV
Ha2meV = Ha2eV * 1000
Ry2eV = codata.value('Rydberg constant times hc in eV')
Ha2Ry = 2.0
Ry2Ha = 0.5
Ha2K = codata.value('hartree-kelvin relationship')

# length conversions
bohr2angstrom = codata.value('Bohr radius') * 1e10
angstrom2bohr = 1 / bohr2angstrom

_conversion_factors = {
    'angstrom': {
        'angstrom': 1,
        'bohr': angstrom2bohr,
    },
    'bohr': {
        'bohr': 1,
        'angstrom': bohr2angstrom,
    },
    'Ha': {
        'Ha': 1,
        'eV': Ha2eV,
        'Ry': Ha2Ry,
    },
    'Ry': {
        'Ha': 1./2,
        'Ry': 1,
        'eV': Ry2eV
    }
}


def convert_units(a, from_units, to_units, inverse=False, copy=True):
    """
    Convert units using predefined unit names and conversion factors

    Parameters
    ----------
    a : array_like
    from_units : str
        from unit
    to_units : str
        to unit
    copy : bool, optional
        flag to copy the input array, or convert the units in-place (copy=False)

    """
    a = np.asarray(a)
    if copy:
        a = np.copy(a)

    if inverse:
        a *= 1./_conversion_factors[from_units][to_units]
    else:
        a *= _conversion_factors[from_units][to_units]

    return a


def crystal2cartesian(coords, lattice_vectors):
    """
    Convert vectors expressed in crystal coordinates to Cartesian coordinates

    Parameters
    ----------
    coords: ndarray, shape (..., npts, 3)
    lattice_vectors: ndarray, shape (3, 3)

    Returns
    -------
    ndarray

    """

    return np.dot(coords, lattice_vectors)


def cartesian2crystal(coords, lattice_vectors):
    """
    Convert vectors expressed in Cartesian coordinates to crystal coordinates

    Parameters
    ----------
    coords: ndarray, shape (..., npts, 3)
    lattice_vectors: ndarray, shape (3, 3)

    Returns
    -------
    ndarray

    """

    return np.dot(coords, np.linalg.inv(lattice_vectors))


def bweights(bvectors):
    distances = np.sqrt(np.sum(bvectors[0]**2, axis=1))
    shells = np.unique(np.round(distances, decimals=6))
    bvec_shells = [bvectors[0][abs(distances - shell) < 5e-7] for shell in shells]

    amat = np.zeros((6, len(shells)))
    for (ish, bvecs) in enumerate(bvec_shells):
        bmat = np.array([np.einsum('i,j->ij', x, y) for x, y in zip(bvecs, bvecs)])
        bmat = np.sum(bmat, axis=0)
        amat[:, ish] = bmat[np.triu_indices(3)]

    [U, s, V] = np.linalg.svd(amat, full_matrices=False)
    bweights_tmp = reduce(np.dot, [np.transpose(V), np.diag(1.0/s), np.transpose(U), np.eye(3)[np.triu_indices(3)]])
    bweights = np.concatenate(tuple([np.ones(len(bvec_shells[ish]))*bweights_tmp[ish] for ish in range(len(shells))]))

    return bweights
