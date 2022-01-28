# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.renderer.mark
import tests.feedback_.renderer


def test_renderer_select_source_master116_toc(tmpdir, master116):
    """Ensure that toc lines are printed justifieded and as a result of
    this, the dots are printed over the whole line."""
    page = 4
    with tests.feedback_.renderer.render_and_open(
            tmpdir,
            master116,
            page=page,
    ) as source:

        toc_lines = source.count('text-align-last:justify')
        assert toc_lines >= 28, toc_lines


# @pytest.mark.xfail(reason='broken header parser')
def test_renderer_select_source_master116_startofcontent(tmpdir, master116):
    """Ensure that `start of content/soc` which means the offset between
    pagetextnavigator and pagetextcontentnavigator is handled properly
    and `1. Einleitung` is marked with red background."""
    page = 8
    marks = feedback.renderer.mark.PageMarkConfiguration(page=8, linemarks={0})
    with tests.feedback_.renderer.render_and_open(
            tmpdir,
            master116,
            marks=marks,
            css=r'#line8_0{background:red};',
            page=page,
    ) as source:
        lines = source.splitlines()
        # ensure that `1 .Einleitung` is marked with `line8_0`
        match = [
            '<span id="line8_0">' in line and '1. Einleitung' in line
            for line in lines
        ]
        assert any(match), source
