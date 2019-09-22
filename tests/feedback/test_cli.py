# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import feedback
import feedback.cli
import feedback.command.decider.border
import tests.resources


# pylint:disable=unused-argument
def test_run_feedback(testdir, monkeypatch):
    cmd = ['-i', tests.resources.RESTRUCTED, '-o', '.']

    utila.run_command(
        cmd,
        monkeypatch=monkeypatch,
        process=feedback.PACKAGE,
        main=feedback.cli.main,
        success=True,
    )
