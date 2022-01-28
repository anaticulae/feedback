# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

import feedback.renderer.shape

RENDER_BOXES_BORDER_STYLE = configo.HV_STR(default='1px solid black')

RENDER_PAGEBORDER_STYLE = configo.HV_STR(default='1px dotted gray')


def render_boxes(page):
    if not page.boxes:
        return []
    result = []
    for index, item in enumerate(page.boxes):
        box = feedback.renderer.shape.render_rectangle(
            item.box,
            border=RENDER_BOXES_BORDER_STYLE,
            reference=f'page_{page.page}_boxed_{index}',
        )
        result.append(box)
    return result


def render_pageborder(page):
    if not page.border:
        return []
    width, height = page.pagesize
    # TODO: CREATE BORDER TO RECTANGLE METHOD
    rectangle = (
        page.border[0],
        page.border[2],
        width - page.border[1],
        height - page.border[3],
    )
    border = feedback.renderer.shape.render_rectangle(
        rectangle,
        border=RENDER_PAGEBORDER_STYLE,
        reference=f'page_{page.page}_border_content',
    )
    return [border]
