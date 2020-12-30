"""Wannier90 I/O routines pertaining to WIN files"""

import sys
import re

import numpy as np

from . import _utils
from ._orbitals2 import orbitals
from ._utils import cartesian2crystal


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
    r'MP_GRID\s+[=:]?\s+(?P<nk1>\d+)\s+(?P<nk2>\d+)\s+(?P<nk3>\d+)\s+',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )

projections_regex = re.compile(
    r'BEGIN\s+PROJECTIONS\s+'
    r'(?P<units>BOHR|ANG)?\s*'
    r'(?P<projections>.+)'
    r'END\s+PROJECTIONS',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )

proj_line_regex = re.compile(
    r'(?P<site>[^:]+):(?P<ang_mtm>[^:]+):?'
    r'(:(?P<zaxis>z=[^:]):)?'
    r'((?P<xaxis>x=[^:]):)?'
    '',
    re.VERBOSE
    )

spinors_regex = re.compile(
    'spinors\s+=\s+(T|.TRUE.)',
    re.VERBOSE | re.IGNORECASE | re.DOTALL
    )
spin_regex = re.compile(r'[(](?P<up>u)?,?(?P<dn>d)?[)]')
quant_dir_regex = re.compile(r'[\[](?P<quant_dir>.+)[\]]$')


def remove_comments(s):
    return re.compile(r'([!]|[#]).*$', re.MULTILINE).sub('', s)


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
        taus.append(np.array(list(map(float, line.split()[1:]))))

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


def read_proj_line(line, dlv, basis, spinors):
    basis_symbols = [x[0] for x in basis]
    basis_vectors = [x[1] for x in basis]

    # print(line)
    zaxis = np.array([0, 0, 1])
    xaxis = np.array([1, 0, 0])
    radial = 1
    zona = 1
    spin = [1, -1]
    quant_dir = np.array([0, 0, 1])

    line = line.replace(' ', '')

    if spin_regex.search(line) is not None:
        spin = []
        if spin_regex.search(line).group('u') is not None: spin.append(1)
        if spin_regex.search(line).group('d') is not None: spin.append(-1)
    line = re.sub(spin_regex.pattern, '', line)

    if quant_dir_regex.search(line):
        quant_dir = np.fromstring(quant_dir_regex.search(line).group('quant_dir'))
    line = re.sub(quant_dir_regex.pattern, '', line)

    parts = line.split(':')

    if parts[0][0] == 'c':
        center = [cartesian2crystal(np.fromstring(parts[0].split('=')[1], sep=','), dlv)]
    elif parts[0][0] == 'f':
        center = [np.fromstring(parts[0].split('=')[1], sep=',')]
    else:
        symbol = parts[0]
        center = [basis_vectors[i] for i in range(len(basis)) if symbol == basis_symbols[i]]

    orbitals_lmr = []
    for orbital in parts[1].split(';'):
        if orbital in list(orbitals.values()):
            tmp = [(l, mr) for (l, mr) in orbitals if orbitals[(l, mr)] == orbital]
            if len(tmp) > 1: raise Exception
            l, mr = tmp[0]
            if mr == 0:
                if l > 0:
                    for i in range(1, 2*l+1+1):
                        orbitals_lmr.append((l, i))
                if l < 0:
                    for i in range(1, abs(l)+1+1):
                        orbitals_lmr.append((l, i))
            else:
                orbitals_lmr.append((l, mr))
        elif re.compile('l=(?P<l>[-]?\d),?(mr=(?P<mr>(\d,?)+))?').match(orbital):
            match = re.compile('l=(?P<l>[-]?\d),?(mr=(?P<mr>(\d,?)+))?').match(orbital)
            for mr in match.group('mr').split(','):
                orbitals_lmr.append((int(match.group('l')), int(mr)))
        else:
            raise ValueError('orbital specification "%s" not recognized' % orbital)

    # sort angular momentum states
    orbitals_lmr = sorted(orbitals_lmr)

    if len(parts) > 2:
        for part in parts[2:]:
            if part.startswith('z='):
                zaxis = np.fromstring(part.split('=')[1], sep=',')
            if part.startswith('x='):
                xaxis = np.fromstring(part.split('=')[1], sep=',')
            if part.startswith('r='):
                radial = int(part.split('=')[1])
            if part.startswith('zona='):
                zona = float(part.split('=')[1])

    projections_line = []
    if spinors:
        for c in center:
            for (l, mr) in orbitals_lmr:
                for s in spin:
                    proj = {
                        'center': c,
                        'l': l,
                        'mr': mr,
                        'z-axis': zaxis/np.linalg.norm(zaxis),
                        'x-axis': xaxis/np.linalg.norm(xaxis),
                        'r': radial,
                        'zona': zona,
                        'spin': s,
                        'spin-axis': quant_dir/np.linalg.norm(quant_dir),
                        'orbital': orbitals[(l, mr)],
                    }
                    projections_line.append(proj)
    else:
        for c in center:
            for (l, mr) in orbitals_lmr:
                proj = {
                    'center': c,
                    'l': l,
                    'mr': mr,
                    'z-axis': zaxis/np.linalg.norm(zaxis),
                    'x-axis': xaxis/np.linalg.norm(xaxis),
                    'r': radial,
                    'zona': zona,
                    'spin': None,
                    'spin-axis': None,
                    'orbital': orbitals[(l, mr)],
                }
                projections_line.append(proj)

    return projections_line


def read_projections(fname):
    with open(fname, 'r') as f:
        contents = f.read()
    contents = remove_comments(contents)

    spinors = spinors_regex.search(contents) is not None
    match = projections_regex.search(contents)

    if match.group('units') is not None:
        units = {'ANG': 'angstrom', 'BOHR': 'bohr'}[match.group('units').upper()]
    else:
        units = 'angstrom'
    dlv = read_dlv(fname, units)

    basis = read_atoms(fname)

    projections = []
    for line in match.group('projections').rstrip('\n').split('\n'):
        if line:
            projections.extend(read_proj_line(line, dlv, basis, spinors))

    return projections


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
