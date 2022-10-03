# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import feedback.renderer.html
import feedback.renderer.loader


@utilatest.requires(power.DOCU009_PDF)
def test_render_boxes(td):
    source = power.link(power.DOCU009_PDF)
    data = feedback.renderer.loader.from_path(source, pages=1)[0]
    html = feedback.renderer.html.render_page(data)

    outpath = os.path.join(td.tmpdir, 'index.html')
    with utilatest.open_webbrowser(outpath):
        utila.file_create(outpath, html)
