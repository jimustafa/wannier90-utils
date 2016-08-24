"""Wannier90 I/O routines pertaining to NNKP files"""
from __future__ import absolute_import, division, print_function
import re

import numpy as np

from ._orbitals import orbitals
from . import _utils


def read_dlv(fname, units='bohr'):
    pattern = re.compile(r'(?:begin\s+real_lattice)(.+)(?:end\s+real_lattice)', re.IGNORECASE | re.DOTALL)
    with open(fname, 'r') as f:
        match = pattern.search(f.read())
        if match is None:
            raise Exception

    dlv = np.fromstring(match.group(1), sep='\n').reshape((3, 3))

    dlv = _utils.convert_units(dlv, 'angstrom', units)

    return dlv


def read_rlv(fname, units='bohr'):
    pattern = re.compile(r'(?:begin\s+recip_lattice)(.+)(?:end\s+recip_lattice)', re.IGNORECASE | re.DOTALL)
    with open(fname, 'r') as f:
        match = pattern.search(f.read())
        if match is None:
            raise Exception

    rlv = np.fromstring(match.group(1), sep='\n').reshape((3, 3))

    rlv = _utils.convert_units(rlv, 'angstrom', units, inverse=True)

    return rlv


def read_kpoints(fname, units='crystal'):
    pattern = re.compile(r'(?:begin\s+kpoints)(?:\s+(?P<nkpts>[0-9]+)\s+)(?P<kpoints>.+)(?:end\s+kpoints)', re.IGNORECASE | re.DOTALL)
    with open(fname, 'r') as f:
        match = pattern.search(f.read())
        if match is None:
            raise Exception

    nkpts = int(match.group('nkpts'))
    kpoints = np.fromstring(match.group('kpoints'), sep='\n').reshape((nkpts, 3))

    if units == 'crystal':
        pass
    elif units == 'angstrom' or units == 'bohr':
        rlv = read_rlv(fname, units)
        kpoints = np.dot(kpoints, rlv)

    return kpoints


def read_projections(fname):
    pattern = re.compile(r'(?:begin\s+(?P<spinor>spinor_)?projections)(?:\s+(?P<nproj>[0-9]+)\s+)(?P<projections>.+)(?:end\s+(?P=spinor)?projections)', re.IGNORECASE | re.DOTALL)
    with open(fname, 'r') as f:
        match = pattern.search(f.read())
        if match is None:
            raise Exception

    nproj = int(match.group('nproj'))
    spinors = match.group('spinor') is not None
    raw_data = np.fromstring(match.group('projections'), sep='\n')

    if not spinors:
        raw_data = np.reshape(raw_data, (nproj, 13))
    else:
        raw_data = np.reshape(raw_data, (nproj, 17))

    # create list of projections
    # each projection is a dictionary
    projections = []
    for iproj in range(len(raw_data)):
        proj = {}
        proj['center'] = raw_data[iproj][:3]
        proj['l'] = l = int(raw_data[iproj][3])
        proj['mr'] = mr = int(raw_data[iproj][4])
        proj['r'] = int(raw_data[iproj][5])
        proj['z-axis'] = raw_data[iproj][6:9]
        proj['x-axis'] = raw_data[iproj][9:12]
        proj['zona'] = raw_data[iproj][12]
        proj['spin'] = int(raw_data[iproj][13]) if spinors else None
        proj['spin-axis'] = raw_data[iproj][14:] if spinors else None
        proj['orbital'] = orbitals[l][mr]

        projections.append(proj)

    return projections


def read_nnkpts(fname):
    pattern = re.compile(r'(?:begin\s+nnkpts)(?:\s+(?P<nntot>[0-9]+)\s+)(?P<nnkpts>.+)(?:end\s+nnkpts)', re.IGNORECASE | re.DOTALL)
    with open(fname, 'r') as f:
        match = pattern.search(f.read())
        if match is None:
            raise Exception

    nntot = int(match.group('nntot'))
    raw_data = np.fromstring(match.group('nnkpts'), sep='\n', dtype=int).reshape((-1, 5))

    kpb_kidx = raw_data[:, 1].reshape((-1, nntot)) - 1
    kpb_g = raw_data[:, 2:].reshape((-1, nntot, 3))

    return kpb_kidx, kpb_g


def read_bvectors(fname, units='angstrom'):
    rlv = read_rlv(fname, units=units)
    kpoints = read_kpoints(fname)
    kpb_kidx, kpb_g = read_nnkpts(fname)

    kpb = kpoints[kpb_kidx]

    bvectors = kpb + kpb_g - kpoints[:, np.newaxis, :]
    bvectors = np.einsum('kbi,ij->kbj', bvectors, rlv)

    return bvectors


def read_excluded_bands(fname):
    pattern = re.compile(r'(?:begin\s+exclude_bands)(.+)(?:end\s+exclude_bands)', re.IGNORECASE | re.DOTALL)
    with open(fname, 'r') as f:
        match = pattern.search(f.read())
        if match is None:
            raise Exception

    bnd_idx = np.fromstring(match.group(1), sep='\n')[1:]
    bnd_idx -= 1

    return bnd_idx
