# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import feedback.utils.multiple_styles

# threshold to avoid invalid sups as a result of bad pdf printing.
THRESHOLD_RISE = configo.HV_FLOAT_PLUS(2.0).value


def render_inline(styles) -> feedback.utils.multiple_styles.Styles:
    result = []
    for style in styles:
        start, end, size, rise, family, flags = style
        fontstyle = style_fromflags(flags)
        fontfamily = f'font-family:{family};'
        first = f'<span style="font-size:{size}px;{fontfamily}{fontstyle}">'
        close = '</span>'
        if rise > THRESHOLD_RISE:
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
    return result


def style_range(textcontainer, start, end, fontstore: iamraw.FontStore):
    # start, end, size, rise, font = style
    result = []
    for item in textcontainer.style.content:
        (start_, end_, size_, rise_, font_) = (
            item.start,
            item.end,
            item.size,
            item.rise,
            item.font,
        )
        if start_ < start:
            continue
        if start_ >= end:
            continue
        end_ = utila.mins(end_, end)  # shrink upper border
        font = fontstore[font_]
        flags = list(font.flags) if font.flags else []
        if font.style == iamraw.Style.ITALIC:
            flags.append(iamraw.FontFlag.ITALIC)
        style = (start_, end_, size_, rise_, font.name, tuple(flags))
        result.append(style)
    return result


def style_fromflags(flags: iamraw.FontFlags) -> str:
    if not flags:
        return ''
    result = ''
    if iamraw.FontFlag.ITALIC in flags:
        result += 'font-style:italic;'
    if iamraw.FontFlag.FORCEBOLD in flags:
        result += 'font-weight:bold;'
    if iamraw.FontFlag.SERIF in flags:
        result += 'font-family:sans-serif;'
    # if iamraw.FontFlag.Symbolic in flags:
    #     result += 'font-family:Consolas;'
    if iamraw.FontFlag.SMALLCAP in flags:
        result += 'font-variant:small-caps;'
    return result
