"""Wannier90 I/O library"""
from __future__ import absolute_import, division, print_function
import collections

from ._amn import *
from ._bands import *
from ._chk import *
from ._eig import *
from ._hr import *
from ._mmn import *
from ._unk import *
from . import nnkp
from . import postw90
from . import utils
from . import win
from . import wout
from . import _utils


Wannier90Data = collections.namedtuple(
    'Wannier90Data',
    [
        'dlv', 'rlv',
        'amn', 'mmn', 'eig',
        'kpoints', 'kpb_kidx', 'kpb_g',
        'bv', 'bw',
        'length_unit', 'energy_unit'
    ])


def read_data(seedname='wannier', **kwargs):
    """
    Read all Wannier90 input data files from the current directory.

    Parameters
    ----------
    seedname : str, optional
        seedname for the Wannier90 files, the default is "wannier"

    """
    dlv = kwargs.get('dlv', nnkp.read_dlv(seedname+'.nnkp', units='angstrom'))
    rlv = kwargs.get('rlv', nnkp.read_rlv(seedname+'.nnkp', units='angstrom'))
    try:
        amn = kwargs['amn']
    except KeyError:
        amn = read_amn(seedname+'.amn')
    try:
        mmn = kwargs['mmn']
    except KeyError:
        mmn = read_mmn(seedname+'.mmn')
    try:
        eig = kwargs['eig']
    except KeyError:
        eig = read_eig(seedname+'.eig')
    kpoints = kwargs.get('kpoints', nnkp.read_kpoints(seedname+'.nnkp'))
    kpb_kidx = kwargs.get('kpb_kidx', nnkp.read_nnkpts(seedname+'.nnkp')[0])
    kpb_g = kwargs.get('kpb_kidx', nnkp.read_nnkpts(seedname+'.nnkp')[1])
    bv = kwargs.get('bv', nnkp.read_bvectors(seedname+'.nnkp', units='angstrom'))
    bw = kwargs.get('bw', _utils.bweights(bv))

    return Wannier90Data(
        dlv=dlv,
        rlv=rlv,
        amn=amn,
        mmn=mmn,
        eig=eig,
        kpoints=kpoints,
        kpb_kidx=kpb_kidx,
        kpb_g=kpb_g,
        bv=bv,
        bw=bw,
        length_unit='angstrom',
        energy_unit='eV',
        )
