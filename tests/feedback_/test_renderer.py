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
from tests.feedback_.fixtures import masterpage72  # pylint:disable=W0611


def test_renderer_load(masterpage72):  # pylint:disable=W0621
    assert masterpage72


def test_renderer_firstpage(testdir, masterpage72):  # pylint:disable=W0621
    outpath = os.path.join(str(testdir), 'firstpage.html')
    firstpage = utila.select_page(masterpage72, 0)

    rendered = feedback.renderer.html.render_page(firstpage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)


def test_renderer_secondpage_mark_line_and_words(testdir, masterpage72):  # pylint:disable=W0621
    outpath = os.path.join(str(testdir), 'secondpage.html')
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
