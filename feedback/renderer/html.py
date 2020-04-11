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
import iamraw.path
import serializeraw
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

    lines = []
    lines.extend(feedback.renderer.boxes.render_pageborder(page))
    lines.extend(feedback.renderer.boxes.render_boxes(page))

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
        lines.append(html)

    if shapes:
        rendered = feedback.renderer.shape.render(shapes)
        lines.extend(rendered)

    if page.images:
        rendered = render_images(page.images)
        lines.extend(rendered)

    if page.horizontals:
        rendered = feedback.renderer.lines.render_horizontals(
            horizontals=page.horizontals,
            page=page.page,
        )
        lines.extend(rendered)

    content = '\n'.join(lines)
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
    result = (f'<div id="page{page}" '
              f'style="position:relative; width:{dimension[0]}px; '
              f'height:{dimension[1]}px; border:1px solid black; '
              'pointer-events:none;">\n'
              f'{html}\n'
              '</div>')
    return result


def load(  # pylint:disable=R0914
        text: str,
        textposition: str,
        fontheader: str = None,
        fontcontent: str = None,
        boxes: str = None,
        hits: str = None,
        images: list = None,
        horizontals: str = None,
        pages: tuple = None,
) -> feedback.renderer.content.HTMLPageContents:
    """Load data to present as html view.

    images: there are more than one images folder possible
    """
    assert all((isinstance(item, str) or item is None)
               for item in [text, textposition, boxes, hits, horizontals])

    text = serializeraw.load_document(text, pages=pages)
    textposition = serializeraw.load_textpositions(textposition, pages=pages)
    boxes = serializeraw.load_boxes(boxes, pages=pages) if boxes else None
    if horizontals:
        horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    hits = serializeraw.load_hits(hits, pages=pages) if hits else None
    if images:
        images = [
            feedback.renderer.images.zip_images(item, pages) for item in images
        ]
        images = utila.flatten(images)
    result = []
    fontstore = None
    if fontheader:
        fontstore = serializeraw.create_fontstore(
            fontheader,
            fontcontent,
            pages=pages,
        )
    for current in text.pages:
        page = current.page
        position = utila.select_page(textposition, page)
        page_boxes = utila.select_page(boxes, page) if boxes else None
        # expected border which are violated by hits
        border = utila.select_page(hits, page).border if hits else None
        hori = utila.select_page(horizontals, page) if horizontals else None
        if hori:
            hori = hori.content
        # skip non TextContainer boxes - for example LTRect
        selected = [
            item for item in current.children
            if isinstance(item, iamraw.TextContainer)
        ]
        fill_fonts(selected, page, fontstore)
        for index, children in enumerate(selected):
            # update with loaded text position
            children.box = position.content[index][0]
        pageimages = feedback.renderer.images.select_images(images, page)
        item = feedback.renderer.content.HTMLPageContent(
            border=border,
            content=selected,
            dimension=text.dimension,
            horizontals=hori,
            images=pageimages,
            page=page,
        )
        if page_boxes:
            item.boxes.extend(page_boxes.content)  # pylint:disable=E1101
        result.append(item)
    return result


def from_path(
        path: str,
        pages: tuple = None,
) -> feedback.renderer.content.HTMLPageContents:
    assert os.path.exists(path), str(path)
    text = iamraw.path.text(path)
    textposition = iamraw.path.textposition(path)
    fontheader = iamraw.path.fontheader(path)
    fontcontent = iamraw.path.fontcontent(path)
    boxes = iamraw.path.boxed(path)
    horizontals = iamraw.path.horizontals(path)
    hits = os.path.join(path, 'decider_border__detection_hits.yaml')
    # make border rendere optional
    fontheader = fontheader if os.path.exists(fontheader) else None
    fontcontent = fontcontent if os.path.exists(fontcontent) else None
    hits = hits if os.path.exists(hits) else None
    boxes = boxes if os.path.exists(boxes) else None
    horizontals = horizontals if os.path.exists(horizontals) else None
    # TODO: INVESTIGATE HERE
    images = [os.path.join(path, 'rawmaker__images_images')]
    loaded = load(
        boxes=boxes,
        fontcontent=fontcontent,
        fontheader=fontheader,
        hits=hits,
        horizontals=horizontals,
        images=images,
        text=text,
        textposition=textposition,
        pages=pages,
    )
    return loaded


def fill_fonts(text, page, fontstore: iamraw.FontStore):
    # TODO: MOVE THIS HACK/ IS THIS A HACK?
    if not fontstore:
        return
    for container_id, container in enumerate(text):
        for line_id, line in enumerate(container):
            for char_id, char in enumerate(line):
                fontid = fontstore.fontid(page, container_id, line_id, char_id)
                font = fontstore[fontid]
                flags = list(font.flags)
                if font.style == iamraw.Style.ITALIC:
                    flags.append(iamraw.FontFlag.Italic)
                char.flags = tuple(flags)
                char.font = font.name
