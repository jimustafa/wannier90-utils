import numpy as np


__all__ = ['read_amn', 'write_amn']


def read_amn(fname):
    """
    Read AMN file.

    Parameters
    ----------
    fname : str

    Returns
    -------
    amn : ndarray, shape (nkpts, nbnds, nproj)

    """
    with open(fname, 'r') as f:
        f.readline()    # header
        [nbnds, nkpts, nproj] = list(map(int, f.readline().split()))
        data_str = f.read()

    raw_data = np.fromstring(data_str, sep='\n').reshape((nkpts*nbnds*nproj, 5))
    amn = raw_data[:, 3] + 1j*raw_data[:, 4]
    amn = np.copy(np.transpose(amn.reshape((nbnds, nproj, nkpts), order='F'), axes=(2, 0, 1)), order='C')

    return amn


def write_amn(fname, amn, header='HEADER'):
    r"""
    Write :math:`A^{(\mathbf{k})}_{mn}` to AMN file.

    Parameters
    ----------
    fname : str
    amn : ndarray, shape (nkpts, nbnds, nproj)
    header : str

    """
    (nkpts, nbnds, nproj) = amn.shape
    indices = np.mgrid[:nbnds, :nproj, :nkpts].reshape((3, -1), order='F') + 1
    amn = np.transpose(amn, axes=(1, 2, 0)).flatten(order='F').view(float).reshape((-1, 2))
    data_out = np.column_stack((indices.transpose(), amn))
    with open(fname, 'w') as f:
        print(header, file=f)
        print('%13d%13d%13d' % (nbnds, nkpts, nproj), file=f)
        np.savetxt(f, data_out, fmt='%5d%5d%5d%18.12f%18.12f')
