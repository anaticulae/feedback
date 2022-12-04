# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider.example
import power
import pytest
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

# pylint:disable=W0611
from tests.fixtures import bachelor56
from tests.fixtures import bachelor128page10
from tests.fixtures import leftright
from tests.fixtures import master116
from tests.fixtures import masterpage72

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(__file__)

RESOURCES = [
    (power.BACHELOR090_PDF, ':'),
    (power.DISS264_PDF, '0:30'),
    (power.HOME025_PDF, '0:10'),
    (power.MASTER072_PDF, ':'),
    (power.MASTER116_PDF, '0:20,100:117'),
    power.BACHELOR028_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR128_PDF,
    power.BOOK007_PDF,
    power.DOCU009_PDF,
    power.DOCU027_PDF,
]
WORKER = utilatest.worker_count(6, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(files):
    decider.example.extract(
        files=files,
        dest=power.generated(),
        pages='0:20',
        worker=WORKER,
        morefeatures=[
            'decider_border',
            'decider_textflow',
        ],
        full=True,
    )
