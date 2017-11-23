from __future__ import absolute_import, division, print_function
import os

import pytest
import numpy as np

from w90utils import io as w90io


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_dlv(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    dlv_ref = w90io.nnkp.read_dlv('wannier.nnkp', units='bohr')
    dlv = w90io.win.read_dlv('wannier.win', units='bohr')

    assert np.allclose(dlv, dlv_ref)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_atoms(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    basis_ref = [x for x in w90io.wout.read_centers_xyz('wannier_centres.xyz') if x[0] != 'X']
    basis = w90io.win.read_atoms('wannier.win', units='angstrom')

    for (symbol_ref, tau_ref), (symbol, tau) in zip(basis_ref, basis):
        assert symbol == symbol_ref
        assert np.allclose(tau, tau_ref)


@pytest.mark.parametrize('example', [('example%02d' % i) for i in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20]])
def test_read_projections(data_dir, example):
    os.chdir(os.path.join(data_dir, example))
    proj_win = w90io.win.read_projections('wannier.win')
    proj_nnkp = w90io.nnkp.read_projections('wannier.nnkp')

    assert len(proj_win) == len(proj_nnkp)

    for i, (proj1, proj2) in enumerate(zip(proj_nnkp, proj_win)):
        for key in proj1:
            assert key in proj2

        try:
            assert np.allclose(proj1['center'], proj2['center'], atol=1e-5)
            assert proj1['l'] == proj2['l']
            assert proj1['mr'] == proj2['mr']
            assert np.allclose(proj1['z-axis'], proj2['z-axis'])
            assert np.allclose(proj1['x-axis'], proj2['x-axis'])
            assert proj1['r'] == proj2['r']
            assert np.allclose(proj1['zona'], proj2['zona'])
            if proj1['spin'] is None:
                assert proj2['spin'] is None
            else:
                assert proj1['spin'] == proj2['spin']
            if proj2['spin-axis'] is None:
                assert proj2['spin-axis'] is None
            else:
                assert np.allclose(proj1['spin-axis'], proj2['spin-axis'])

        except AssertionError:
            print(i)
            print(proj1)
            print(proj2)
            raise


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_kpoints(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    kpoints_ref = w90io.nnkp.read_kpoints('wannier.nnkp')
    kpoints = w90io.win.read_kpoints('wannier.win')

    assert np.allclose(kpoints, kpoints_ref)
