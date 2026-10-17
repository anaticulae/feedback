# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import feedback.renderer.shape


def render(lines):
    if len(lines) < 22:  # TODO: WORKAROUND
        return []
    lines = utilo.unique_lines(lines)
    lines = [item for item in lines if not utilo.isdot(item)]
    lines = [utilo.round_line(*item) for item in lines]
    result = []
    for line in lines:
        rendered = feedback.renderer.shape.render_line(line)
        result.append(rendered)
    return result
