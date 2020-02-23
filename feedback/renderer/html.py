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
import os

import iamraw
import rawmaker.path
import serializeraw
import utila

import feedback.renderer.content
import feedback.renderer.mark
import feedback.renderer.shape


def render_page(
        page: feedback.renderer.content.HTMLPageContent,
        marks: feedback.renderer.mark.PageMarkConfiguration = None,
        shapes: list = None,
) -> str:
    """Convert `page`-data to raw html data.

    If page.border is defined, the content border is added and a
    reference to access these rectangle is added (see referece).

    If page.boxes contains some rectangles, there are rendered as black
    boxes.
    """
    if marks is None:
        marks = feedback.renderer.mark.PageMarkConfiguration()
    wordmarker = feedback.renderer.mark.WordMarker(page.page, marks.wordmarks)
    linemarker = feedback.renderer.mark.LineMarker(page.page, marks.linemarks)

    lines = []
    for line in page.content:
        marked = wordmarker.markme(line.text)
        marked = linemarker.markme(marked)
        html = create_line(line, marked)
        lines.append(html)

    if shapes:
        rendered = feedback.renderer.shape.render(shapes)
        lines.extend(rendered)

    lines.extend(render_pageborder(page))
    lines.extend(render_boxes(page))

    content = '\n'.join(lines)
    result = create_pagebox(content, page.page, page.dimension)
    return result


def render_pageborder(page):
    if not page.border:
        return []
    # TODO: CREATE BORDER TO RECTANGLE METHOD
    rectangle = (
        page.border[0],
        page.border[2],
        page.border[1],
        page.border[3],
    )
    # TODO: Think about style concept, USE HOLY VALUE?
    border = feedback.renderer.shape.render_rectangle(
        rectangle,
        border='1px dotted gray',
        reference=f'page_{page.page}_border_content',
    )
    return [border]


def render_boxes(page):
    if not page.boxes:
        return []
    result = []
    for index, item in enumerate(page.boxes):
        box = feedback.renderer.shape.render_rectangle(
            item.box,
            border='1px solid black',
            reference=f'page_{page.page}_boxed_{index}',
        )
        result.append(box)
    return result


def create_line(line, rawline):
    size = line.lines[0].chars[0].size
    position = f'top: {line.box.y0}px; left: {line.box.x0}px;'
    location = f'position:absolute; {position}'
    fontsize = f'font-size:{size}px'
    rawline = rawline.replace('\n', '<br>')
    result = f'<span style="{location} {fontsize}">{rawline}</span>'
    return result


def create_pagebox(html: str, page: int, dimension) -> str:
    result = (f'<div id="page{page}" '
              f'style="position:relative; width:{dimension[0]}px; '
              f'height:{dimension[1]}px; border:1px solid black;">\n'
              f'{html}\n'
              '</div>')
    return result


def load(
        text: str,
        textposition: str,
        boxes: str = None,
        hits: str = None,
        pages: tuple = None,
) -> list:
    text = serializeraw.load_document(text, pages=pages)
    textposition = serializeraw.load_textpositions(textposition, pages=pages)
    boxes = serializeraw.load_boxes(boxes, pages=pages) if boxes else None
    hits = serializeraw.load_hits(hits, pages=pages) if hits else None
    result = []
    for current in text.pages:
        page = current.page
        position = utila.select_page(textposition, page)
        page_boxes = utila.select_page(boxes, page) if boxes else None
        border = utila.select_page(hits, page).border if hits else None
        # skip non TextContainer boxes - for example LTRect
        selected = [
            item for item in current.children
            if isinstance(item, iamraw.TextContainer)
        ]
        for index, children in enumerate(selected):
            # update with loaded text position
            children.box = position.content[index]

        item = feedback.renderer.content.HTMLPageContent(
            page=page,
            dimension=text.dimension,
            content=selected,
            border=border,
        )
        if page_boxes:
            item.boxes.extend(page_boxes.content)  # pylint:disable=E1101
        result.append(item)
    return result


def from_path(path: str, pages: tuple = None) -> list:
    assert os.path.exists(path), str(path)
    text = rawmaker.path.text(path)
    textposition = rawmaker.path.textposition(path)
    boxes = rawmaker.path.boxed(path)
    hits = os.path.join(path, 'decider_border__detection_hits.yaml')
    # make border rendere optional
    hits = hits if os.path.exists(hits) else None
    boxes = boxes if os.path.exists(boxes) else None
    loaded = load(text, textposition, boxes=boxes, hits=hits, pages=pages)
    return loaded
