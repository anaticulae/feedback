# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import tests


def test_finding_feature(testdir, monkeypatch):
    pdf = power.BACHELOR090_PDF
    source = power.link(pdf)
    cmd = f'--findings -i {source} --pdf {pdf} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert utila.file_count(testdir.tmpdir, ext='png') >= 8
