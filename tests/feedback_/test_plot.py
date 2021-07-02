# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import painter
import power
import utila
import utilatest

import tests.feedback_


@utilatest.requires(power.BACHELOR090_PDF)
def test_render_findings_histogram(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i {source} --plot'
    tests.feedback_.run(cmd, monkeypatch=monkeypatch)
    rendered = utila.file_read_binary('feedback__plot_findings_histogram.png')
    assert len(rendered) > 1000


@utilatest.requires(power.BACHELOR090_PDF)
def test_render_findings_pie(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i {source} --plot'
    tests.feedback_.run(cmd, monkeypatch=monkeypatch)
    rendered = utila.file_read_binary('feedback__plot_findings_types_pie.png')
    assert len(rendered) > 1000
    painter.show_figure(rendered)
