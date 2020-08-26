# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider.example
import power
import pytest

import feedback
import tests.resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = feedback.PACKAGE

RESOURCES = [
    (tests.resources.MASTER116_PDF, '0:20,100:117'),
    tests.resources.BACHELOR90_PDF,
    (power.DISS264_PDF, '0:30'),
    tests.resources.BACHELOR56_PDF,
    tests.resources.LEFTRIGHT,
    tests.resources.MASTER72_PDF,
    tests.resources.PORTING_PYTHON3_PDF,
    tests.resources.RESTRUCTED_PDF,
    (power.HOMEWORK025_PDF, '0:10'),
]

WORKER = 6


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(tests.resources.REQUIRED_RESOURCES)


def extract(files):
    # TODO: ENABLE SIMPLE PATH REPOSITORY PATTERN LATER
    decider.example.extract(
        files + [power.REPOSITORY],
        power.generated(),
        '0:20',
        worker=WORKER,
    )
