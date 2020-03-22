import os

import pytest
import numpy as np

import w90utils
from w90utils import io as w90io


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_data(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    if example == 'example01':
        w90io.read_data(eig=None)
    else:
        w90io.read_data()


@pytest.mark.parametrize('example', ['example03', 'example04'])
def test_eig_io(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    eig_ref = w90io.read_eig('wannier.eig')

    with open('test.eig', 'w') as f:
        w90io.write_eig('test.eig', eig_ref)
    eig = w90io.read_eig('test.eig')

    assert np.allclose(eig, eig_ref)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_amn(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    a = w90io.read_amn('wannier.amn')

    test_lines = []
    with open('wannier.amn', 'r') as f:
        lines = f.readlines()
        for i in [4, 7, 12, 29, 67, 113]:
            test_lines.append(lines[i].strip())

    for line in test_lines:
        m = int(line.split()[0]) - 1
        n = int(line.split()[1]) - 1
        ikpt = int(line.split()[2]) - 1
        x = complex(float(line.split()[3]), float(line.split()[4]))
        assert(abs(a[ikpt][m][n] - x) < 1e-12)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_write_amn(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    a_ref = w90io.read_amn('wannier.amn')
    w90io.write_amn('wannier.amn_test', a_ref)
    a_test = w90io.read_amn('wannier.amn_test')

    assert np.allclose(a_test, a_ref)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example04'])
def test_read_mmn(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    kpb_kidx_ref, kpb_g_ref = w90io.nnkp.read_nnkpts('wannier.nnkp')
    m, kpb_kidx, kpb_g = w90io._mmn._process_mmn_file('wannier.mmn')

    assert np.all(kpb_kidx == kpb_kidx_ref)
    assert np.all(kpb_g == kpb_g_ref)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example04'])
def test_write_mmn(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    m_ref, kpb_kidx_ref, kpb_g_ref = w90io._mmn._process_mmn_file('wannier.mmn')
    w90io.write_mmn('wannier.mmn_test', m_ref, kpb_kidx_ref, kpb_g_ref)

    m, kpb_kidx, kpb_g = w90io._mmn._process_mmn_file('wannier.mmn_test')

    assert np.all(kpb_kidx == kpb_kidx_ref)
    assert np.all(kpb_g == kpb_g_ref)
    assert np.allclose(m, m_ref)

    # with open('wannier.mmn', 'r') as f:
    #     lines_ref = f.readlines()
    # with open('wannier.mmn_test', 'r') as f:
    #     lines_test = f.readlines()

    # for line1, line2 in zip(lines_test[1:], lines_ref[1:]):
    #     try:
    #         assert line1 == line2
    #     except AssertionError:
    #         print()
    #         print(line1)
    #         print(line2)
    #         raise


@pytest.mark.parametrize('example', ['example02', 'example03', 'example04'])
def test_read_hr(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    Hmn, Rvectors, Rweights = w90io.read_hr('wannier_hr.dat')

    with open('wannier_hr.dat', 'r') as f:
        lines = f.readlines()
        nwann = int(lines[1])
        nrpts = int(lines[2])

        (q, r) = divmod(nrpts, 15)
        ndegen_lines = q if r == 0 else q+1
        nheader_lines = ndegen_lines + 3

        lines = lines[nheader_lines:]

        for iln in [15, 16, 31, 32, 74, 93, 154, 234, 302]:
            line = lines[iln]
            (q, r) = divmod(iln+1, nwann**2)
            irvec = q if r == 0 else q+1
            irvec -= 1
            x = np.fromstring(line, sep=' ')
            m = int(x[3]) - 1
            n = int(x[4]) - 1
            hr_val = complex(x[5], x[6])
            assert(abs(Hmn[irvec, m, n] - hr_val) < 1e-6)


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_chkpt(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    a = w90io.read_amn('wannier.amn')
    m = w90io.read_mmn('wannier.mmn')
    chkpt = w90io.CheckpointIO('wannier.chk')
    assert chkpt.nkpts == a.shape[0]
    assert chkpt.nbnds == a.shape[1]
    assert chkpt.nwann == a.shape[2]
    assert chkpt.nntot == m.shape[1]


@pytest.mark.parametrize('example', ['example01', 'example02'])
def test_read_chkpt_mats(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    chkpt = w90io.CheckpointIO('wannier.chk')

    w90dat = w90io.read_data(eig=None)
    umn = chkpt.umat
    mmn_chkpt = chkpt.mmat
    mmn = w90utils.rotate_mmn(w90dat.mmn, umn, w90dat.kpb_kidx)

    assert np.allclose(mmn_chkpt, mmn)


@pytest.mark.parametrize('example', ['example03', 'example04'])
def test_read_bands(data_dir, example):
    os.chdir(os.path.join(data_dir, example))

    bands_ref = w90io.postw90.read_bands('wannier_geninterp.dat')
    bands = w90io.read_bands('wannier_band.dat')

    assert np.allclose(bands, bands_ref, rtol=0, atol=1e-4)
