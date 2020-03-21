import os

import pytest
import numpy as np

from w90utils import io as w90io


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_centers(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    centers_ref = w90io.CheckpointIO('wannier.chk').wannier_centers
    centers = np.asarray([x[1] for x in w90io.wout.read_centers_xyz('wannier_centres.xyz') if x[0] == 'X'])

    assert np.allclose(centers, centers_ref)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_conv(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    conv = w90io.wout.read_conv('wannier.wout')
    sprd = w90io.wout.read_sprd('wannier.wout')

    assert np.allclose(sprd['TOT'], conv['spread'])


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_sprd(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    sprd = w90io.wout.read_sprd('wannier.wout')
    chkpt = chkpt = w90io.CheckpointIO('wannier.chk')

    assert np.allclose(sprd['TOT'][-1], np.sum(chkpt.wannier_spreads))
