# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider.example
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

# pylint:disable=W0611
from tests.fixtures import bachelor56
from tests.fixtures import bachelor128page10
from tests.fixtures import leftright
from tests.fixtures import master116
from tests.fixtures import masterpage72

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    (hoverpower.BACHELOR090_PDF, ':'),
    (hoverpower.DISS264_PDF, '0:30'),
    (hoverpower.HOME025_PDF, '0:10'),
    (hoverpower.MASTER072_PDF, ':'),
    (hoverpower.MASTER116_PDF, '0:20,100:117'),
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR056_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.BOOK007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU027_PDF,
]
WORKER = utilotest.worker_count(6, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(files):
    decider.example.extract(
        files=files,
        dest=hoverpower.generated(),
        pages='0:20',
        worker=WORKER,
        morefeatures=[
            'decider_border',
            'decider_textflow',
        ],
        full=True,
    )
