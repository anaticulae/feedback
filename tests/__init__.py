# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import inspect
import os
import sys

import feedback

TEST_PATH = os.path.join(feedback.ROOT, 'tests')
assert os.path.exists(TEST_PATH)


def single_execution():
    """Check that test method is executed as single test. You can use
    this method to open the result in a web browser if test is executed
    with a human in front of the machine eg. as a single test."""
    # TODO: MOVE TO UTILA TEST
    frame = inspect.currentframe()
    parent = inspect.getouterframes(frame)[1]
    caller = parent.function
    return all([item in sys.argv for item in ['-k', caller]])
