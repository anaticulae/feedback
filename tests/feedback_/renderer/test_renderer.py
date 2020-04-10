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

import utila

import feedback.renderer.html
import feedback.renderer.mark
from tests.feedback_.fixtures import bachelor56  # pylint:disable=W0611
from tests.feedback_.fixtures import leftright  # pylint:disable=W0611
from tests.feedback_.fixtures import masterpage72  # pylint:disable=W0611


def test_renderer_load(masterpage72):  # pylint:disable=W0621
    assert masterpage72


def test_renderer_firstpage(tmpdir, masterpage72):  # pylint:disable=W0621
    outpath = os.path.join(tmpdir, 'firstpage.html')
    firstpage = utila.select_page(masterpage72, 0)

    rendered = feedback.renderer.html.render_page(firstpage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)


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
    outpath = os.path.join(tmpdir, 'firstpage.html')
    firstpage = utila.select_page(leftright, 0)

    shapes = [
        {
            'type': 'rectangle',
            'bounding': (50, 50, 400, 400),
            'border': '1px solid red',
        },
    ]

    rendered = feedback.renderer.html.render_page(firstpage, shapes=shapes)
    assert len(rendered) > 300, str(rendered)
    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)


def test_renderer_toc(tmpdir, masterpage72):  # pylint:disable=W0621
    """This test aims to generate and view a toc very fast to check
    develop new html renderings."""
    outpath = os.path.join(tmpdir, 'tocpage.html')
    tocpage = utila.select_page(masterpage72, 1)

    rendered = feedback.renderer.html.render_page(tocpage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)


def test_render_page_with_horizontals(tmpdir, masterpage72):  # pylint:disable=W0621
    """Render footnote separator."""
    outpath = os.path.join(tmpdir, 'index.html')
    footnote_separator = utila.select_page(masterpage72, 3)

    rendered = feedback.renderer.html.render_page(footnote_separator)
    assert len(rendered) > 300, str(rendered)
    assert '<hr' in rendered, str(rendered)

    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)


def test_render_bachelor56_title_page(tmpdir, bachelor56):  # pylint:disable=W0621
    outpath = os.path.join(tmpdir, 'index.html')
    titlepage = utila.select_page(bachelor56, 0)

    rendered = feedback.renderer.html.render_page(titlepage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)
