import numpy as np


__all__ = ['read_hr']


def read_hr(fname):
    with open(fname, 'r') as f:
        contents = f.readlines()

    # header = contents[0]
    nwann = int(contents[1].strip())
    nrpts = int(contents[2].strip())

    nints_per_line = 15     # as indicated in Wannier90 User Guide Sec. 8.18
    # determine the number of lines the degeneracies span
    ndegen_lines = nrpts // nints_per_line
    if nrpts % 15 != 0:
        ndegen_lines += 1

    # read the degeneracy data
    rdegen = np.fromstring(''.join(contents[3:3+ndegen_lines]), sep='\n')

    istart_hr = 3+ndegen_lines
    raw_data = np.fromstring(''.join(contents[istart_hr:]), sep='\n').reshape((-1, 7))

    hr = raw_data[:, 5] + 1j*raw_data[:, 6]
    hr = hr.reshape((nrpts, nwann**2)).reshape((nrpts, nwann, nwann), order='F')
    hr = np.copy(hr, order='C')

    Rvectors = np.copy(raw_data[:, :3].astype(int)[::nwann**2], order='C')
    Rweights = 1 / rdegen

    return hr, Rvectors, Rweights
