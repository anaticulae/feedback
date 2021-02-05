# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The feedback generates the central document view"""

import functools

import utilatest

import feedback
import feedback.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=feedback.cli.main,
    process=feedback.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=feedback.cli.main,
    process=feedback.PROCESS,
    success=False,
)
