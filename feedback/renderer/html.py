# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import serializeraw
import utila

import feedback.renderer
import feedback.renderer.mark


def render_page(
        page: feedback.renderer.HTMLPageContent,
        marks: feedback.renderer.mark.PageMarkConfiguration = None,
) -> str:
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
    content = '\n'.join(lines)
    result = create_pagebox(content, page.page, page.dimension)
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


def load(text: str, textposition: str, pages: tuple = None) -> list:
    text = serializeraw.load_document(text, pages=pages)
    textposition = serializeraw.load_textpositions(textposition, pages=pages)
    result = []
    for current in text.pages:
        page = current.page
        position = utila.select_page(textposition, page)
        # skip non TextContainer boxes - for example LTRect
        selected = [
            item for item in current.children
            if isinstance(item, iamraw.TextContainer)
        ]
        for index, children in enumerate(selected):
            # update with loaded text position
            children.box = position.content[index]

        item = feedback.renderer.HTMLPageContent(
            page=page,
            dimension=text.dimension,
            content=selected,
        )
        result.append(item)
    return result


def from_path(path: str, pages: tuple = None) -> list:
    assert os.path.exists(path), str(path)
    text = os.path.join(path, 'rawmaker__text_text.yaml')
    textposition = os.path.join(path, 'rawmaker__text_positions.yaml')
    loaded = load(text, textposition, pages=pages)
    return loaded
