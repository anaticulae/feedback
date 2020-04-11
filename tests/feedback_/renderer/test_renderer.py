# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import webbrowser

import pytest
import utila

import feedback.renderer.html
import feedback.renderer.mark
import tests.feedback_.renderer as tfr
from tests.feedback_.fixtures import bachelor56  # pylint:disable=W0611
from tests.feedback_.fixtures import leftright  # pylint:disable=W0611
from tests.feedback_.fixtures import masterpage72  # pylint:disable=W0611


def test_renderer_load(masterpage72):  # pylint:disable=W0621
    assert masterpage72


@pytest.mark.xfail(reason='duplicated horizontal line rendering')
def test_renderer_firstpage(tmpdir, masterpage72):  # pylint:disable=W0621
    with tfr.render_and_open(tmpdir, masterpage72, 0) as html:
        assert '<hr' not in html, html


def test_renderer_secondpage_mark_line_and_words(tmpdir, masterpage72):  # pylint:disable=W0621
    # TODO: VERIFY WITH SELENIUM
    outpath = os.path.join(tmpdir, 'secondpage.html')
    secondpage = utila.select_page(masterpage72, 1)

    marks = feedback.renderer.mark.PageMarkConfiguration(
        page=1,
        wordmarks=set([1, 2, 3, 4, 5]),
        linemarks=set([4, 5, 20]),
    )

    rendered = feedback.renderer.html.render_page(secondpage, marks=marks)
    assert len(rendered) > 300, str(rendered)

    style = """\
        <style>
        #line1_20{
            background:red;
        }
        </style>
        """
    output = style + rendered
    utila.file_create(outpath, output)

    if utila.single_execution():
        webbrowser.open(outpath)


def test_renderer_shapes_mark_bounding(tmpdir, leftright):  # pylint:disable=W0621
    """Render first page of `leftright` example and add a red rectangle
    in the top center of the page."""
    shapes = [
        {
            'type': 'rectangle',
            'bounding': (50, 50, 400, 400),
            'border': '1px solid red',
        },
    ]
    with tfr.render_and_open(tmpdir, leftright, page=0, shapes=shapes) as html:
        assert '1px solid red' in html  # ensure to render red box


@utila.todo(major=3, minor=2, description='verify with selenium')
def test_renderer_toc(tmpdir, masterpage72):  # pylint:disable=W0621
    """This test aims to generate and view a toc very fast to check
    develop new html renderings."""
    with tfr.render_and_open(tmpdir, masterpage72, page=1):
        # check that page number are on vertical line
        pass


def test_render_page_with_horizontals(tmpdir, masterpage72):  # pylint:disable=W0621
    """Render footnote separator."""
    with tfr.render_and_open(tmpdir, masterpage72, page=3) as html:
        assert '<hr' in html, str(html)


def test_render_bachelor56_title_page(tmpdir, bachelor56):  # pylint:disable=W0621
    with tfr.render_and_open(tmpdir, bachelor56, page=0) as html:
        # ensure to render university logo
        assert '<img src=' in html, html


def test_render_bachelor56_italic_style(tmpdir, bachelor56):  # pylint:disable=W0621
    with tfr.render_and_open(tmpdir, bachelor56, page=5) as html:
        assert 'font-style:italic;' in html, str(html)


def test_render_bachelor56_render_table(tmpdir, bachelor56):  # pylint:disable=W0621
    with tfr.render_and_open(tmpdir, bachelor56, page=15) as html:
        pass
