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
    inpath = os.path.join(tests.resources.GENERATED_MASTER_PAGE72)
    root = str(testdir)
    tests.feedback_.run(f'-i {inpath} -o {root} --view', monkeypatch=monkeypatch) # yapf:disable
