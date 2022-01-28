# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.renderer.shape


def render_horizontals(horizontals, page):
    if not horizontals:
        return []
    result = []
    for index, item in enumerate(horizontals):
        x0, y0 = item.box[0], item.box[1]
        # TODO: FIX THIS OFFSET?
        y0 = y0 - 10
        width = item.box[2] - item.box[0]
        line = feedback.renderer.shape.render_horizontal(
            x0=x0,
            y0=y0,
            width=width,
            reference=f'page_{page}_line_{index}',
        )
        result.append(line)
    return result
