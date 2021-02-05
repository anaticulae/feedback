# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.renderer.shape


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
    # TODO: Think about style concept, USE HOLY VALUE?
    border = feedback.renderer.shape.render_rectangle(
        rectangle,
        border='1px dotted gray',
        reference=f'page_{page.page}_border_content',
    )
    return [border]
