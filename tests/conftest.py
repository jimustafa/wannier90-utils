from __future__ import absolute_import, division, print_function
import os
import shutil

import pytest


@pytest.fixture(scope='session')
def data_dir(tmpdir_factory):
    data_dir = os.path.join(os.path.dirname(__file__), './_data')
    for example_dir in [('example%02d' % i) for i in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20]]:
        shutil.copytree(os.path.join(data_dir, example_dir), os.path.join(str(tmpdir_factory.getbasetemp()), example_dir))

    return str(tmpdir_factory.getbasetemp())
