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

import feedback

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = feedback.PACKAGE

power.setup(feedback.ROOT)

RESOURCES = [
    (power.MASTER116_PDF, '0:20,100:117'),
    (power.BACHELOR090_PDF, '0:30'),
    (power.BACHELOR128_PDF, '0:20'),
    power.MASTER072_PDF,
    power.BACHELOR056_PDF,
    (power.DISS264_PDF, '0:30'),
    power.DOCU027_PDF,
    power.DOCU009_PDF,
    power.BOOK007_PDF,
    (power.HOME025_PDF, '0:10'),
]

WORKER = 6


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(files):
    config = dict(decider.example.SELECTED)
    config['figureo'] = True
    decider.example.extract(
        files=files,
        destination=power.generated(),
        pages='0:20',
        worker=WORKER,
        base=power.REPOSITORY,
        selected=config,
        morefeatures=[
            'decider_border',
        ],
    )
