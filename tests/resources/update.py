# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import decider.example
import detector.feature.titlepage
import utila

import feedback
import feedback.utils
import tests.resources


def install_requirements():
    utila.clean_install(feedback.ROOT, feedback.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    # ensure that generation folder exists
    if os.path.exists(tests.resources.GENERATED):
        # generate only once, to reduce
        return

    os.makedirs(tests.resources.GENERATED, exist_ok=True)

    files = [
        tests.resources.RESTRUCTED_PDF,
        tests.resources.PORTING_PYTHON3_PDF,
        tests.resources.MASTER_72_PAGE_NOIMAGES_PDF,
    ]
    decider.example.extract(files, tests.resources.GENERATED)
