"""Wannier90 I/O routines pertaining to WOUT files"""

import numpy as np


def read_centers_xyz(fname):
    with open(fname, 'r') as f:
        contents = f.readlines()

    centers = []
    for line in contents[2:]:
        symbol = line.split()[0]
        tau = np.array(list(map(float, line.split()[1:])))

        centers.append((symbol, tau))

    return centers


def read_conv(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    conv_data = []
    data_lines = []
    for line in lines:
        if line.strip().endswith('CONV'):
            data_lines.append(line)

    conv_data = np.array([list(map(float, line.split()[:4])) for line in data_lines[3:]])
    conv_data = dict(list(zip(['iter', 'delta', 'gradient', 'spread', 'time'], conv_data.T)))
    conv_data['iter'] = conv_data['iter'].astype(int)

    return conv_data


def read_sprd(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    sprd_data = {'D': [], 'OD': [], 'TOT': []}
    for line in lines:
        if line.strip().endswith('SPRD'):
            data = line.split()
            sprd_data['D'].append(float(data[1]))
            sprd_data['OD'].append(float(data[3]))
            sprd_data['TOT'].append(float(data[5]))

    return sprd_data
