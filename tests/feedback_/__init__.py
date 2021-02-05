# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The feedback generates the central document view"""

import utilatest

import feedback
import feedback.cli


def run(cmd: str, monkeypatch):
    utilatest.run_command(
        cmd,
        process=feedback.PACKAGE,
        main=feedback.cli.main,
        success=True,
        monkeypatch=monkeypatch,
    )
