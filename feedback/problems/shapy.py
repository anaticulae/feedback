# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

SHAPY = {}


def determine_shapes(findings, page):
    if not findings:
        return []
    # select findings on `page`
    findings = [
        item for item in findings
        if item.location and item.location.page == page
    ]
    result = []
    for item in findings:
        try:
            renderer = SHAPY[item.msgid]
            rendered = renderer(item)
            result.append(rendered)
        except KeyError:
            continue
    return result


def error_2020(item) -> dict:
    bounding = item.location.value
    # TODO: REMOVE AFTER FIXING COORDINATES
    ytop = min([bounding[3], bounding[1]])
    ybottom = max([bounding[3], bounding[1]])
    bounding_reverse = (bounding[0], ytop, bounding[2], ybottom)
    result = {
        'type': 'rectangle',
        'bounding': bounding_reverse,
        'border': '1px solid red',
        'reference': f'finding_{item.number}'
    }
    return result


SHAPY[2020] = error_2020
