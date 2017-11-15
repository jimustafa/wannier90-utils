from __future__ import absolute_import, division, print_function
import os

import pytest
import numpy as np

from w90utils import io as w90io


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_projections(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    w90io.nnkp.read_projections('wannier.nnkp')


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_excluded_bands(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    idx_ref = w90io.CheckpointIO('wannier.chk').bands_excl - 1
    idx = w90io.nnkp.read_excluded_bands('wannier.nnkp')

    assert np.all(idx == idx_ref)
