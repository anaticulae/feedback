# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module aims to print different additional shapes on html pages
to highlight an error message.

For example - to highlight that a border was crossed, a rectangle as
virtual border is painted."""

import iamraw
import utila


def render(items: list) -> list:
    result = []
    for item in items:
        typ = item['type']
        item = item.copy()
        item.pop('type')
        rendered = None
        if typ == 'rectangle':
            rendered = render_rectangle(**item)
        assert rendered, f'unsupported: {typ}'
        result.append(rendered)
    return result


# pointer-events: do not catch any pointer event cause we print the
# rectangle above the content and afterwards no selection is possible.
# Hint: a negative z-index is no option, cause the backgrounds of parent
# element hides this z-negative content.
RECTANGLE = """\
<span {reference} style="position:absolute;
top:{y0}px;left:{x0}px;width:{width}px;height:{height}px;
border:{border}; background:{background}; pointer-events: none;
{more}"></span>"""


def render_rectangle(
        bounding: iamraw.BoundingBox,
        border: str = '1px solid black',
        background: str = 'transparent',
        more: str = '',
        reference: str = None,
) -> str:
    """Render html rectangle represented as `<span>`."""
    bounding = utila.roundme(*bounding)  # reduce digits in html output
    x0 = bounding[0]
    y0 = bounding[1]
    assert y0 <= bounding[3], str(bounding)
    assert x0 <= bounding[2], str(bounding)
    width = bounding[2] - bounding[0]
    height = bounding[3] - bounding[1]
    reference = '' if reference is None else f'id="{reference}"'
    rendered = RECTANGLE.format(
        background=background,
        border=border,
        height=height,
        more=more,
        reference=reference,
        width=width,
        x0=x0,
        y0=y0,
    )
    return rendered


LINE = """\
<svg {reference} style="position:absolute; top:{y0}px;left:{x0}px;
width:{width}px;height:{height}px;pointer-events: none; {more}" fill="none">
<line x1="0" y1="0" x2="{width}" y2="{height}" stroke="black"></line></svg>
"""


def render_line(
        bounding: iamraw.BoundingBox,
        border: str = '1px solid black',
        more: str = '',
        reference: str = None,
) -> str:
    bounding = utila.roundme(*bounding)  # reduce digits in html output
    x0, y0, x1, y1 = bounding
    assert y0 <= y1, str(bounding)
    assert x0 <= x1, str(bounding)
    height = y1 - y0
    width = x1 - x0
    height = max([height, 1])
    width = max([width, 1])
    rendered = RECTANGLE.format(
        border=border,
        height=height,
        more=more,
        reference=reference,
        width=width,
        x0=x0,
        y0=y0,
    )
    return rendered
