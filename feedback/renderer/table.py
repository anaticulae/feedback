# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import utila

import feedback.renderer.shape


def render(lines):
    if len(lines) < 22:  # TODO: WORKAROUND
        return []
    lines = make_unique(lines)
    lines = [item for item in lines if not dot(item)]
    lines = [remove_wanking(item) for item in lines]
    result = []
    for line in lines:
        rendered = feedback.renderer.shape.render_line(line)
        result.append(rendered)
    return result


def remove_wanking(item):
    # TODO: IMPROVE NAME
    x0, y0, x1, y1 = utila.roundme(item, digits=0)
    if math.fabs(x0 - x1) < 4.0:
        x1 = x0
    if math.fabs(y0 - y1) < 4.0:
        y1 = y0

    return (x0, y0, x1, y1)


def make_unique(items: list) -> list:
    # TODO: MOVE TO UTILA
    result = []
    for item in items:
        if any((equals(item, it) for it in result)):
            continue
        result.append(item)
    return result


def equals(first, second, diff: float = 3.0) -> bool:
    # TODO: MOVE TO UTILA
    if distance(first[0], first[1], second[0], second[1]) > diff:
        return False
    if distance(first[2], first[3], second[2], second[3]) > diff:
        return False
    return True


def dot(item) -> bool:
    return distance(item[0], item[1], item[2], item[3]) <= 3.0


def distance(x0, y0, x1, y1) -> float:
    return math.sqrt(pow(x1 - x0, 2) + pow(y1 - y0, 2))
