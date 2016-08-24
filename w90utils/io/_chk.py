from __future__ import absolute_import, division, print_function
import contextlib
import cStringIO as StringIO

import numpy as np
from scipy.io import FortranFile


__all__ = ['CheckpointIO']


class CheckpointIO(object):
    def __init__(self, fname=None, auto_read=True):
        if fname and auto_read:
            self.from_file(fname)

    def from_file(self, fname):
        with FortranFile(fname, 'r') as f:
            self.header = ''.join(f.read_record('c'))
            self.nbnds = f.read_ints()[0]
            self.nbnds_excl = f.read_ints()[0]
            self.bands_excl = f.read_ints()
            self.dlv = f.read_reals().reshape((3, 3), order='F')
            self.rlv = f.read_reals().reshape((3, 3), order='F')
            self.nkpts = f.read_ints()[0]
            self.grid_dims = f.read_ints()
            self.kpoints = f.read_reals().reshape((-1, 3))
            self.nntot = f.read_ints()[0]
            self.nwann = f.read_ints()[0]
            self.chkpt = f.read_record('c')
            self.disentanglement = bool(f.read_ints()[0])

            if self.disentanglement:
                self.omega_invariant = f.read_reals()[0]
                self.windows = f.read_ints().reshape((self.nbnds, self.nkpts), order='F').transpose
                f.read_ints()
                self.umat_opt = np.transpose(f.read_reals().view(complex).reshape((self.nbnds, self.nwann, self.nkpts), order='F'), axes=(2, 0, 1))

            self.umat = np.transpose(f.read_reals().view(complex).reshape((self.nwann, self.nwann, self.nkpts), order='F'), axes=(2, 0, 1))
            self.mmat = np.transpose(f.read_reals().view(complex).reshape((self.nwann, self.nwann, self.nntot, self.nkpts), order='F'), axes=(3, 2, 0, 1))
            self.wannier_centers = f.read_reals().reshape((-1, 3))
            self.wannier_spreads = f.read_reals()

    def __str__(self):
        with contextlib.closing(StringIO.StringIO()) as sio:
            print(self.header, file=sio)
            print(self.nbnds, file=sio)
            print(self.nbnds_excl, file=sio)
            print(self.dlv, file=sio)
            print(self.rlv, file=sio)
            print(self.nkpts, file=sio)
            s = sio.getvalue()
        return s
