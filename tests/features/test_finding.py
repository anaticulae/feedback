# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utila
import utilatest

import tests


@utilatest.requires(power.BACHELOR090_PDF)
def test_finding_feature(testdir, monkeypatch):
    pdf = power.BACHELOR090_PDF
    source = power.link(pdf)
    cmd = f'--findings  --pdf {pdf} -i {source} -o {testdir.tmpdir}'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert utila.file_count(testdir.tmpdir, ext='png') >= 8


@utilatest.requires(power.BACHELOR028_PDF)
def test_finding_sentence_bachelor028(testdir, monkeypatch):
    pdf = power.BACHELOR028_PDF
    source = power.link(pdf)
    cmd = f'--findings  --pdf {pdf} -i {source} --pages=7'
    tests.run(cmd, monkeypatch=monkeypatch)
    assert utila.file_count(testdir.tmpdir, ext='png') >= 1
    findings = protocol.load_grouped(
        source=utila.join(source, '__optimized__'),
        pages=(7,),
    )[0].content
    finding = protocol.select_findings(findings, msgid=7605)[0]
    expected = testdir.tmpdir.join(f'{finding.number}.png')
    assert utila.exists(expected)
