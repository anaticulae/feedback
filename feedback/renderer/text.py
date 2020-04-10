# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import feedback.utils.multiple_styles


def render_inline(line) -> feedback.utils.multiple_styles.Styles:
    assert isinstance(line, iamraw.Line), type(line)
    # TODO: SUPPORT FONT SIZE AND RISE
    chars = line.chars
    grouped = [[chars[0]]]
    for item in chars[1:]:
        if item.size != grouped[-1][-1].size:
            grouped.append([item])
        else:
            grouped[-1].append(item)
    result = []
    index = 0
    for chunk in grouped:
        start = index
        end = start + len(chunk)
        first = f'<span style="font-size:{chunk[0].size}px">'
        last = '</span>'
        result.append(
            feedback.utils.multiple_styles.Style(
                start,
                end,
                first,
                last,
            ))
        index += len(chunk)
    return result
