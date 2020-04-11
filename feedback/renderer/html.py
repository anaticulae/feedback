# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""HTML View
=========

References
----------

* page_{number}_border_content: access content border to change
                                appereance, show/hide etc.
"""

import iamraw
import utila

import feedback.renderer.boxes
import feedback.renderer.content
import feedback.renderer.images
import feedback.renderer.lines
import feedback.renderer.mark
import feedback.renderer.shape
import feedback.renderer.text
import feedback.utils.multiple_styles


def render_page(
        page: feedback.renderer.content.HTMLPageContent,
        marks: feedback.renderer.mark.PageMarkConfiguration = None,
        shapes: list = None,
) -> str:
    """Convert `page`-data to raw html data.

    If page.border is defined, the content border is added and a
    reference to access these rectangle is added (see referece).

    If page.boxes contains some rectangles, there are rendered as black
    thin rectangles.
    """
    assert page, 'page is none, require page to render'
    if marks is None:
        marks = feedback.renderer.mark.PageMarkConfiguration()
    wordmarker = feedback.renderer.mark.WordMarker(page.page, marks.wordmarks)
    linemarker = feedback.renderer.mark.LineMarker(page.page, marks.linemarks)

    raw = []
    raw.extend(feedback.renderer.boxes.render_pageborder(page))
    raw.extend(feedback.renderer.boxes.render_boxes(page))

    for textcontainer in page.content:
        text = textcontainer.text
        styles = []
        marked_words: list = wordmarker.markme(text)
        # feedback.utils.multiple_styles.Style
        marked_lines = linemarker.markme(text)
        if marked_lines:
            styles.append(marked_lines)
        if marked_words:
            styles.extend(marked_words)
        html = create_line(textcontainer, styles)
        raw.append(html)

    if shapes:
        rendered = feedback.renderer.shape.render(shapes)
        raw.extend(rendered)

    if page.images:
        rendered = render_images(page.images)
        raw.extend(rendered)

    if page.horizontals:
        rendered = feedback.renderer.lines.render_horizontals(
            horizontals=page.horizontals,
            page=page.page,
        )
        raw.extend(rendered)

    content = '\n'.join(raw)
    result = create_pagebox(content, page.page, page.dimension)
    return result


def render_images(images):
    result = []
    for _, info, fileimage in images:
        bounding = info.bounding
        width = utila.roundme(info.bounding[2] - info.bounding[0])
        height = utila.roundme(info.bounding[3] - info.bounding[1])
        style = (f'style="position:absolute;border:1px solid black;'
                 f'top:{bounding[1]}px;left:{bounding[0]}px;'
                 f' width:{width}px;height:{height}px"')
        img = (f'<img src="{fileimage}" {style}/>')
        result.append(img)
    return result


def create_line(textcontainer, marked_line) -> str:
    bounding = textcontainer.box
    result = []
    for index, line in enumerate(textcontainer):
        # render multiline text lines
        box = iamraw.split_y(bounding, index, len(textcontainer))
        position = f'top:{box.y0}px;left:{box.x0}px;'
        location = f'position:absolute;{position}'
        line_style = []
        line_style.extend(marked_line)
        fontstyle = feedback.renderer.text.render_inline(line)
        line_style.extend(fontstyle)
        rendered = feedback.utils.multiple_styles.tostring(
            line.text,
            line_style,
        )
        rendered = rendered.replace('\n', '<br>')
        raw = f'<span style="{location}">{rendered}</span>'
        result.append(raw)
    html = ''.join(result)
    return html


def create_pagebox(html: str, page: int, dimension) -> str:
    # pointer-events:none - do not effect mouse cursor handling
    assert dimension, dimension
    result = (f'<div id="page{page}" '
              f'style="position:relative; width:{dimension[0]}px; '
              f'height:{dimension[1]}px; border:1px solid black; '
              'pointer-events:none;">\n'
              f'{html}\n'
              '</div>')
    return result
