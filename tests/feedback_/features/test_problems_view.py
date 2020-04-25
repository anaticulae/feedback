# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import tests.feedback_
import tests.resources


def test_report_problems_view(testdir, monkeypatch):
    inpath = os.path.join(tests.resources.MASTER72_GENERATED)
    root = str(testdir)
    tests.feedback_.run(f'-i {inpath} -o {root} --view', monkeypatch=monkeypatch) # yapf:disable

    outpath = os.path.join(root, 'feedback__view_pages')
    written = list(os.listdir(outpath))
    assert len(written) >= 10, written
