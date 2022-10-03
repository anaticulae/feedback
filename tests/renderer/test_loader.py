# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import feedback.renderer.mark
import tests.renderer


def test_load_navigator_soc(td, bachelor128page10):
    """Ensure that first content line is rendered as line0. Skip header
    content."""
    page = 10
    line = 0
    css = f'#line{page}_{line}' + '{background:red;}'
    pagemarks = feedback.renderer.mark.PageMarkConfiguration(
        page=page,
        linemarks=[line],
    )
    with tests.renderer.render_and_open(
            td.tmpdir,
            bachelor128page10,
            page=page,
            marks=pagemarks,
            css=css,
    ) as source:
        indexes = utila.findindex(source, f'"line{page}_{line}"')
        first, middle, last = (
            utila.findindex(source, 'Im')[0],
            utila.findindex(source, 'zweiten Kapitel')[0],
            utila.findindex(source, 'folgt eine kurze')[0],
        )
        # mark first content line(ptcn) as #line_10_0
        assert indexes[0] <= first <= indexes[1] <= middle <= indexes[2] <= last
