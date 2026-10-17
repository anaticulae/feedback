# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import pytest
import utilo
import utilotest

import tests


@utilotest.nightly
@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_finding_feature(td, mp):
    pdf = hoverpower.BACHELOR090_PDF
    source = hoverpower.link(pdf)
    cmd = f'--findings  --pdf {pdf} -i {source} -o {td.tmpdir}'
    tests.run(cmd, mp=mp)
    assert utilo.file_count(td.tmpdir, ext='png') >= 8


@pytest.mark.xfail(reason='software integration')
@utilotest.requires(hoverpower.BACHELOR028_PDF)
def test_finding_sentence_bachelor028(td, mp):
    pdf = hoverpower.BACHELOR028_PDF
    source = hoverpower.link(pdf)
    cmd = f'--findings  --pdf {pdf} -i {source} --pages=7'
    tests.run(cmd, mp=mp)
    assert utilo.file_count(td.tmpdir, ext='png') >= 1
    findings = protoerror.load_grouped(
        source=utilo.join(source, '__optimized__'),
        pages=(7,),
    )[0].content
    finding = protoerror.select_findings(findings, msgid=7605)[0]
    expected = td.tmpdir.join(f'{finding.number}.png')
    assert utilo.exists(expected)
