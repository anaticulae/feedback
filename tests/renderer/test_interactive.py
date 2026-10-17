# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo
import utilotest

import feedback.renderer.content
import feedback.renderer.html


def test_renderer_interactive_showhide(td):
    """Ensure that `border-reference` is addet to html element."""
    outpath = td.tmpdir.join('index.html')
    html = feedback.renderer.content.HTMLPageContent(
        border=(50, 700, 50, 800),
        page=10,
        pagesize=(800, 1024),
        navigator=[],
    )
    content = feedback.renderer.html.render_page(page=html)
    assert 'page_10_border_content' in content

    with utilotest.open_webbrowser(outpath):
        utilo.file_create(outpath, content)
