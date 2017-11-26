from __future__ import absolute_import, division, print_function
import os

import pytest
import numpy as np

import w90utils
from w90utils import io as w90io


@pytest.mark.parametrize('example', ['example01', 'example02'])
def test_omega_d(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    spread_ref = w90io.wout.read_sprd('wannier.wout')

    w90dat = w90io.read_data(eig=None)
    umn = w90utils.unitarize(w90dat.amn)
    mmn = w90utils.rotate_mmn(w90dat.mmn, umn, w90dat.kpb_kidx)
    spread_d = w90utils.sprd.omega_d(mmn, w90dat.bv, w90dat.bw)

    assert np.allclose(spread_d, spread_ref['D'][0])


@pytest.mark.parametrize('example', ['example01', 'example02'])
def test_omega_od(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    spread_ref = w90io.wout.read_sprd('wannier.wout')

    w90dat = w90io.read_data(eig=None)
    umn = w90utils.unitarize(w90dat.amn)
    mmn = w90utils.rotate_mmn(w90dat.mmn, umn, w90dat.kpb_kidx)
    spread_od = w90utils.sprd.omega_od(mmn, w90dat.bw)

    assert np.allclose(spread_od, spread_ref['OD'][0])


@pytest.mark.parametrize('example', ['example01', 'example02'])
def test_omega(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    spread_ref = w90io.wout.read_sprd('wannier.wout')

    w90dat = w90io.read_data(eig=None)
    umn = w90utils.unitarize(w90dat.amn)
    mmn = w90utils.rotate_mmn(w90dat.mmn, umn, w90dat.kpb_kidx)
    spread_tot_1 = w90utils.sprd.omega(mmn, w90dat.bv, w90dat.bw)

    spread_i = w90utils.sprd.omega_i(mmn, w90dat.bw)
    spread_dod = w90utils.sprd.omega_dod(mmn, w90dat.bv, w90dat.bw)
    spread_tot_2 = spread_dod + spread_i

    spread_i = w90utils.sprd.omega_i(mmn, w90dat.bw)
    spread_d = w90utils.sprd.omega_d(mmn, w90dat.bv, w90dat.bw)
    spread_od = w90utils.sprd.omega_od(mmn, w90dat.bw)
    spread_tot_3 = spread_d + spread_od + spread_i

    assert np.allclose(spread_tot_1, spread_ref['TOT'][0])
    assert np.allclose(spread_tot_2, spread_ref['TOT'][0])
    assert np.allclose(spread_tot_3, spread_ref['TOT'][0])
