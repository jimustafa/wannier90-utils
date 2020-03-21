import os
import shutil

import pytest


example_ids = {
    'wannier90-2.0.1': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20],
    'wannier90-2.1.0': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20],
}


@pytest.fixture(scope='session', params=['wannier90-2.0.1', 'wannier90-2.1.0'])
def data_dir(request, tmpdir_factory):
    data_dir = os.path.join(os.path.dirname(__file__), './_data')
    for example_dir in [('%s/example%02d' % (request.param, i)) for i in example_ids[request.param]]:
        shutil.copytree(os.path.join(data_dir, example_dir), os.path.join(str(tmpdir_factory.getbasetemp()), example_dir))

    return os.path.join(str(tmpdir_factory.getbasetemp()), request.param)
