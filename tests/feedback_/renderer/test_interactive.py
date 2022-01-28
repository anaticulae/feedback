# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utilatest

import feedback.renderer.content
import feedback.renderer.html


def test_renderer_interactive_showhide(testdir):
    """Ensure that `border-reference` is addet to html element."""
    outpath = os.path.join(testdir.tmpdir, 'index.html')
    html = feedback.renderer.content.HTMLPageContent(
        border=(50, 700, 50, 800),
        page=10,
        pagesize=(800, 1024),
        navigator=[],
    )
    content = feedback.renderer.html.render_page(page=html)
    assert 'page_10_border_content' in content

    with utilatest.open_webbrowser(outpath):
        utila.file_create(outpath, content)
