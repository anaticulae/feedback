# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import tests.feedback_


@utilatest.requires(power.MASTER072_PDF)
def test_report_problems_view(testdir, monkeypatch):
    inpath = power.link(power.MASTER072_PDF)
    cmd = f'-i {inpath} -o {testdir.tmpdir} --view'
    tests.feedback_.run(cmd, monkeypatch=monkeypatch)

    outpath = os.path.join(testdir.tmpdir, 'feedback__view_pages')
    written = list(os.listdir(outpath))
    assert len(written) >= 10, written
    # TODO: REMOVE THIS TEST


@utilatest.requires(power.MASTER116_PDF)
def test_view_master116_border_size(testdir, monkeypatch):
    inpath = power.link(power.MASTER116_PDF)
    cmd = f'-i {inpath} -o {testdir.tmpdir} --view '
    tests.feedback_.run(cmd, monkeypatch=monkeypatch)

    outpath = os.path.join(testdir.tmpdir, 'feedback__view_pages')
    written = list(os.listdir(outpath))
    assert len(written) >= 10, written

    # TODO: ADD CHECK FOR CHANGING PAGE DIMENSION
