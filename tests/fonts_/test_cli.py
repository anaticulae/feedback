# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir

import utilatest

from feedback.command.decider.fonts import PROCESS_NAME
from feedback.command.decider.fonts import main
from tests.fonts_ import FONTS_UGLY_DATA


# pylint:disable=unused-argument
def test_fonts_run_main(testdir, monkeypatch):
    cmd = ['-i', FONTS_UGLY_DATA, '-o', '.']

    utilatest.run_command(
        cmd,
        monkeypatch=monkeypatch,
        process=PROCESS_NAME,
        main=main,
        success=True,
    )

    written_files = listdir('.')
    view_and_error_file = 3
    assert len(written_files) == view_and_error_file, str(written_files)
