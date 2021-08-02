# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utilatest

from feedback.renderer.shape import render_rectangle


def test_render_rectangle():
    bounding = (10, 10, 100, 100)
    result = render_rectangle(bounding=bounding)
    assert len(result) > 40, result
    assert '10' in result, result  # position
    assert '90' in result, result  # width


def test_render_overlapping_shapes(testdir):
    # TODO: verify test via SELENIUM
    root = str(testdir)
    outpath = os.path.join(root, 'index.html')

    html = ('<div id="page0" style="position:relative; width:595.32px; '
            'height:841.92px; border:1px solid black;">')
    html += render_rectangle((10, 200, 400, 400))
    html += render_rectangle((100, 20, 200, 300), background='blue')
    html += render_rectangle((33, 33, 199, 99), background='transparent')
    html += '</div>'

    with utilatest.open_webbrowser(outpath):
        utila.file_create(outpath, html)
