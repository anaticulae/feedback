# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

SHAPY = {}


def determine_shapes(findings, page: int) -> list:
    if not findings:
        return []
    selected = utila.select_page(findings, page)
    if not selected:
        return []
    result = []
    for item in selected:
        try:
            renderer = SHAPY[item.msgid]
        except KeyError:
            # no special renderer available
            continue
        rendered = renderer(item)
        result.append(rendered)
    return result


def render_rectangle(item) -> dict:
    bounding = item.location.value
    bounding = utila.rectangle_ensure_bounding(bounding)
    result = {
        'type': 'rectangle',
        'bounding': bounding,
        'border': '1px solid red',
        'reference': f'finding_{item.number}'
    }
    return result


SHAPY[2020] = render_rectangle
SHAPY[2025] = render_rectangle
SHAPY[3030] = render_rectangle
SHAPY[3031] = render_rectangle
SHAPY[4000] = render_rectangle
SHAPY[4001] = render_rectangle
SHAPY[4002] = render_rectangle
SHAPY[4003] = render_rectangle
SHAPY[4004] = render_rectangle
SHAPY[4005] = render_rectangle
SHAPY[7000] = render_rectangle
SHAPY[7770] = render_rectangle
