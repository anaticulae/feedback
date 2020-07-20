# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw

import feedback.utils.multiple_styles

# threshold to avoid invalid sups as a result of bad pdf printing.
THRESHOLD_RISE = configo.HV_FLOAT_PLUS(2.0).value


def render_inline(line) -> feedback.utils.multiple_styles.Styles:
    assert isinstance(line, iamraw.Line), type(line)
    # TODO: SUPPORT FONT SIZE AND RISE
    # TODO: CHECK FONT RISE TOLERANCE TO AVOID TO MANY GROUPS
    chars = line.chars
    grouped = [[chars[0]]]
    for item in chars[1:]:
        last = grouped[-1][-1]
        if any((
                item.size != last.size,
                item.rise != last.rise,
                item.font != last.font,
                item.flags != last.flags,
        )):
            grouped.append([item])
        else:
            grouped[-1].append(item)
    result = []
    index = 0
    for chunk in grouped:
        start = index
        end = start + len(chunk)
        style = styles(chunk[0].flags)
        font = f'font-family:{chunk[0].font};'
        first = f'<span style="font-size:{chunk[0].size}px;{style}{font}">'
        close = '</span>'
        if chunk[0].rise > THRESHOLD_RISE:
            # Threshold is required cause some text is raises a little bit
            # cause of font styling. For example: MARWICK, Alice `!ARWICK`
            # is set a little bit higher than the rest.
            first = f'{first}<sup>'
            close = f'</sup>{close}'
        result.append(
            feedback.utils.multiple_styles.Style(
                start,
                end,
                first,
                close,
            ))
        index += len(chunk)
    return result


def styles(flags: iamraw.FontFlags) -> str:
    if not flags:
        return ''
    result = ''
    if iamraw.FontFlag.Italic in flags:
        result += 'font-style:italic;'
    if iamraw.FontFlag.ForceBold in flags:
        result += 'font-weight:bold;'
    if iamraw.FontFlag.Serif in flags:
        result += 'font-family:sans-serif;'
    if iamraw.FontFlag.Symbolic in flags:
        result += 'font-family:Consolas;'
    if iamraw.FontFlag.SmallCap in flags:
        result += 'font-variant:small-caps;'
    return result
