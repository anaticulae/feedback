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


@utilatest.nightly
@utilatest.requires(power.BACHELOR090_PDF)
def test_finding_feature(td, mp):
    pdf = power.BACHELOR090_PDF
    source = power.link(pdf)
    cmd = f'--findings  --pdf {pdf} -i {source} -o {td.tmpdir}'
    tests.run(cmd, mp=mp)
    assert utila.file_count(td.tmpdir, ext='png') >= 8


@utilatest.requires(power.BACHELOR028_PDF)
def test_finding_sentence_bachelor028(td, mp):
    pdf = power.BACHELOR028_PDF
    source = power.link(pdf)
    cmd = f'--findings  --pdf {pdf} -i {source} --pages=7'
    tests.run(cmd, mp=mp)
    assert utila.file_count(td.tmpdir, ext='png') >= 1
    findings = protocol.load_grouped(
        source=utila.join(source, '__optimized__'),
        pages=(7,),
    )[0].content
    finding = protocol.select_findings(findings, msgid=7605)[0]
    expected = td.tmpdir.join(f'{finding.number}.png')
    assert utila.exists(expected)
