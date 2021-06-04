# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import inspect
import os
import sys
import webbrowser

import utila
import utilatest

import feedback.renderer.html

PATTERN = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{title}</title>
<style>{css}</style>
</head>
<body>
{content}
</body>
</html>
"""


def html(content: str, title: str = 'no title', css: str = None):
    css = css if css else ''
    return PATTERN.format(content=content, title=title, css=css)


@contextlib.contextmanager
def render_and_open(
    directory: int,
    content,
    page: int,
    marks=None,
    shapes=None,
    css=None,
):
    outpath = os.path.join(directory, 'index.html')
    content = utila.select_page(content, page)

    rendered = feedback.renderer.html.render_page(
        content,
        marks=marks,
        shapes=shapes,
    )
    rendered = html(rendered, css=css)
    assert len(rendered) > 300, str(rendered)

    yield rendered

    utila.file_create(outpath, rendered)

    if utilatest.single_execution():
        webbrowser.open(outpath)
