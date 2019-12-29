# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import serializeraw
import utila

import feedback.renderer


def render_page(page: feedback.renderer.HTMLPageContent) -> str:
    result = []
    for line in page.content:
        if not line.text.strip():
            # remove white lines
            continue
        size = line.lines[0].chars[0].size
        position = f'top: {line.box.y0}px; left: {line.box.x0}px;'
        location = f'position:absolute; {position}'
        fontsize = f'font-size:{size}px'
        rawline = line.text.replace('\n', '<br>')
        raw = f'<span style="{location} {fontsize}">{rawline}</span>'
        result.append(raw)

    content = '\n'.join(result)
    result = (f'<div style="position:relative; width:{page.dimension[0]}px; '
              f'height:{page.dimension[1]}px; border:1px solid black;">\n'
              f'{content}'
              '\n</div>')
    return result


def load(path, pages=None) -> list:
    text = os.path.join(path, 'rawmaker__text_text.yaml')
    text = serializeraw.load_document(text, pages=pages)
    text_position = os.path.join(path, 'rawmaker__text_positions.yaml')
    text_position = serializeraw.load_textpositions(text_position, pages=pages)

    result = []
    for current in text.pages:
        page = current.page
        position = utila.select_page(text_position, page)
        position = position.content
        # skip non TextContainer boxes - for example LTRect
        selected = [
            item for item in current.children
            if isinstance(item, iamraw.TextContainer)
        ]
        for index, children in enumerate(selected):
            children.box = position[index]
        item = feedback.renderer.HTMLPageContent(
            page=page,
            dimension=text.dimension,
            content=selected,
        )
        result.append(item)
    return result
