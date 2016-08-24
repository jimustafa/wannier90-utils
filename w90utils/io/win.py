"""Wannier90 I/O routines pertaining to WIN files"""
from __future__ import absolute_import, division, print_function
import sys
import re

import numpy as np

from . import _utils


unit_cell_regex = re.compile(
    r'BEGIN\s+UNIT_CELL_CART\s+'
    r'(?P<units>BOHR|ANG)?'
    r'(?P<dlv>.+)'
    r'END\s+UNIT_CELL_CART\s+',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )

atoms_regex = re.compile(
    r'BEGIN\s+ATOMS_(?P<suffix>(FRAC)|(CART))\s+'
    r'(?P<units>BOHR|ANG)?'
    r'(?P<atoms>.+)'
    r'END\s+ATOMS_(?P=suffix)\s+',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )

kpoints_regex = re.compile(
    r'BEGIN\s+KPOINTS\s+'
    r'(?P<kpoints>.+)'
    r'END\s+KPOINTS\s+',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )

kgrid_regex = re.compile(
    r'MP_GRID\s+(?P<nk1>\d+)\s+(?P<nk2>\d+)\s+(?P<nk3>\d+)\s+',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )


def read_dlv(fname, units='bohr'):
    """
    Read direct lattice vectors from WIN file.

    Parameters
    ----------
    fname : str
        Wannier90 WIN file
    units : str, {'bohr', 'angstrom'}
        units of returned lattice vectors

    Returns
    -------
    dlv : ndarray, shape (3, 3)
        direct lattice vectors

    """
    with open(fname, 'r') as f:
        match = unit_cell_regex.search(f.read())
        if match is None:
            raise Exception

    dlv = np.fromstring(match.group('dlv').strip(), sep='\n').reshape((3, 3))

    if match.group('units') is not None:
        units_win = {'ANG': 'angstrom', 'BOHR': 'bohr'}[match.group('units').upper()]
    else:
        units_win = 'angstrom'

    if units == units_win:
        pass
    elif units in ['bohr', 'angstrom'] and units_win in ['bohr', 'angstrom']:
        dlv = _utils.convert_units(dlv, units_win, units)
    else:
        raise Exception

    return dlv


def read_atoms(fname, units='crystal'):
    with open(fname, 'r') as f:
        match = atoms_regex.search(f.read())
        if match is None:
            raise Exception

    symbols = []
    taus = []
    for line in match.group('atoms').strip().splitlines():
        symbols.append(line.split()[0])
        taus.append(np.array(map(float, line.split()[1:])))

    if match.group('suffix').upper() == 'FRAC':
        units_win = 'crystal'
    else:
        if match.group('units') is not None:
            units_win = {'ANG': 'angstrom', 'BOHR': 'bohr'}[match.group('units').upper()]
        else:
            units_win = 'angstrom'

    taus = np.asarray(taus)

    if units == units_win:
        pass
    elif units == 'crystal' and units_win in ['bohr', 'angstrom']:
        dlv = read_dlv(fname, units=units_win)
        taus = _utils.cartesian2crystal(taus, dlv)
    elif units in ['bohr', 'angstrom'] and units_win == 'crystal':
        dlv = read_dlv(fname, units=units)
        taus = _utils.crystal2cartesian(taus, dlv)
    elif units in ['bohr', 'angstrom'] and units_win in ['bohr', 'angstrom']:
        taus = _utils.convert_units(taus, units_win, units)
    else:
        raise Exception

    basis = list(zip(symbols, taus))

    return basis


def read_kgrid(fname):
    with open(fname, 'r') as f:
        match = kgrid_regex.search(f.read())
        if match is None:
            raise Exception

    kgrid = (int(match.group('nk1')), int(match.group('nk2')), int(match.group('nk3')))

    return kgrid


def read_kpoints(fname):
    with open(fname, 'r') as f:
        match = kpoints_regex.search(f.read())
        if match is None:
            raise Exception

    kpoints = np.fromstring(match.group('kpoints').strip(), sep='\n').reshape((-1, 3))

    return kpoints


def print_unit_cell(dlv, units='bohr', file=sys.stdout):
    units = units.upper()

    print('BEGIN UNIT_CELL_CART', file=file)
    #
    if units == 'BOHR' or 'ANG':
        print(units, file=file)
    else:
        raise ValueError('units must be "bohr" or "ang"')
    #
    np.savetxt(file, dlv, fmt='%18.12f')
    #
    print('END UNIT_CELL_CART', file=file)
    print('', file=file)


def print_atoms(atoms, units='crystal', file=sys.stdout):
    units = units.upper()

    if units == 'CRYSTAL':
        block_label = 'ATOMS_FRAC'
        print('BEGIN ATOMS_FRAC', file=file)
    elif units == 'BOHR' or units == 'ANG':
        block_label = 'ATOMS_CART'
        print('BEGIN ATOMS_CART', file=file)
        print(units, file=file)
    else:
        raise ValueError('units must be "CRYSTAL", "BOHR", or "ANG"')
    #
    for symbol, tau in atoms:
        print('%-5s  ' % symbol, end='', file=file)
        np.savetxt(file, np.asarray(tau).reshape((1, 3)), fmt='%18.12f')
    #
    print('END %s' % block_label, file=file)
    print('', file=file)


def print_kgrid(kgrid, file=sys.stdout):
    print('MP_GRID %3d %3d %3d' % tuple(kgrid), file=file)


def print_kpoints(kpoints, mp_grid=None, file=sys.stdout):
    if mp_grid is not None:
        nkpts = np.prod(mp_grid)
        if nkpts != len(kpoints):
            raise Exception
        print('MP_GRID %3d %3d %3d' % tuple(mp_grid), file=file)
    print('BEGIN KPOINTS', file=file)
    np.savetxt(file, kpoints, fmt='%18.12f')
    print('END KPOINTS', file=file)
