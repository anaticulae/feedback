# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.renderer.shape


def render_lines(page):
    if not page.horizontals:
        return []
    result = []
    for index, item in enumerate(page.horizontals):
        line = feedback.renderer.shape.render_line(
            item.box,
            reference=f'page_{page.page}_line_{index}',
        )
        result.append(line)
    return result
