# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

from tests.resources import REQUIRED_RESOURCES
from tests.resources.update import extract_examples
from tests.resources.update import install_requirements
from tests.resources.update import sync_resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name


def pytest_sessionstart(session):  # pylint:disable=W0613
    if 'PYTEST_XDIST_WORKER' in os.environ:
        return
    # install or use rawmaker
    if 'GENERATE' in os.environ or utila.test.LONGRUN:
        utila.log('install requirements')
        install_requirements()

        utila.log('synchronize test resources')
        sync_resources()

        utila.log('extract resources')
        extract_examples()

    for item in REQUIRED_RESOURCES:
        advice = 'run `baw --test=long` to generate test data'
        msg = f'required test path does not exists: {item}, {advice}'
        assert os.path.exists(item), str(msg)
