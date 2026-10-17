# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import upainter
import utilo
import utilotest

import tests


@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_render_findings_histogram(td, mp):  # pylint:disable=W0613
    source = hoverpower.link(hoverpower.BACHELOR090_PDF)
    cmd = f'-i {source} --plot'
    tests.run(cmd, mp=mp)
    rendered = utilo.file_read_binary('feedback__plot_findings_histogram.png')
    assert len(rendered) > 1000


@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_render_findings_pie(td, mp):  # pylint:disable=W0613
    source = hoverpower.link(hoverpower.BACHELOR090_PDF)
    cmd = f'-i {source} --plot'
    tests.run(cmd, mp=mp)
    rendered = utilo.file_read_binary('feedback__plot_findings_types_pie.png')
    assert len(rendered) > 1000
    upainter.show_figure(rendered)
