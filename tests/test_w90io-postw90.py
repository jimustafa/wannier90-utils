from __future__ import absolute_import, division, print_function
import os

import pytest
import numpy as np

from w90utils import io as w90io


@pytest.mark.parametrize('example', ['example03', 'example04'])
def test_read_bands_kpoints(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    rlv = w90io.nnkp.read_rlv('wannier.nnkp', units='angstrom')

    kpoints_ref = w90io.read_kpoints('wannier_band.kpt')

    kpoints = w90io.postw90.read_bands_kpoints('wannier_geninterp.dat', )
    kpoints = w90io._utils.cartesian2crystal(kpoints, rlv)

    assert np.allclose(kpoints, kpoints_ref)


@pytest.mark.parametrize('example', ['example03', 'example04'])
def test_read_vnk(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    vnk = w90io.postw90.read_vnk('wannier_geninterp.dat')
    raw_data = np.loadtxt('wannier_geninterp.dat')

    if raw_data.shape[1] != 8:
        assert vnk is None
    else:
        assert vnk is not None
