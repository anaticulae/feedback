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


def error_2020(item) -> dict:
    bounding = item.location.value
    bounding = utila.rectangle_ensure_bounding(bounding)
    result = {
        'type': 'rectangle',
        'bounding': bounding,
        'border': '1px solid red',
        'reference': f'finding_{item.number}'
    }
    return result


SHAPY[2020] = error_2020
SHAPY[2025] = error_2020
SHAPY[3030] = error_2020
SHAPY[3031] = error_2020
SHAPY[4000] = error_2020
SHAPY[4001] = error_2020
SHAPY[4002] = error_2020
SHAPY[4003] = error_2020
SHAPY[4004] = error_2020
SHAPY[4005] = error_2020
SHAPY[7000] = error_2020
SHAPY[7770] = error_2020
