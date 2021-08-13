# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module aims to print different additional shapes on html pages
to highlight an error message.

For example - to highlight that a border was crossed, a rectangle as
virtual border is painted.

regression test
---------------

Ensure that width and height is passed correctly
>>> render_rectangle((56.7, 35.35, 527.7, 799.21))
'...width:471.0px;height:763.86px;...'
"""

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
        if typ == 'rectangles':
            rendered = render_rectangles(**item)
        assert rendered, f'unsupported: {typ}'
        result.append(rendered)
    return result


# pointer-events: do not catch any pointer event cause we print the
# rectangle above the content and afterwards no selection is possible.
# Hint: a negative z-index is no option, cause the backgrounds of parent
# element hides this z-negative content.
RECTANGLE = """\
<span {reference} style="position:absolute;z-index:{zindex};
top:{y0}px;left:{x0}px;width:{width}px;height:{height}px;
border:{border};background:{background};pointer-events:none;
{more}"></span>"""


def render_rectangle(
    bounding: iamraw.BoundingBox,
    border: str = '1px solid black',
    background: str = 'transparent',
    more: str = '',
    reference: str = None,
    zindex: int = 10,
) -> str:
    """Render html rectangle represented as `<span>`."""
    reference = html_reference(reference)
    bounding = utila.roundme(*bounding)  # reduce digits in html output
    if not bounding[1] <= bounding[3]:
        utila.error(f'invalid bounding: {bounding}')
    if not bounding[0] <= bounding[2]:
        utila.error(f'invalid bounding: {bounding}')
    bounding = utila.rectangle_ensure_bounding(bounding)
    x0 = bounding[0]
    y0 = bounding[1]
    width = utila.rectangle_width(bounding)
    height = utila.rectangle_height(bounding)
    x0, y0, width, height = utila.roundme(x0, y0, width, height)
    rendered = RECTANGLE.format(
        background=background,
        border=border,
        height=height,
        more=more,
        reference=reference,
        width=width,
        x0=x0,
        y0=y0,
        zindex=zindex,
    )
    return rendered


def render_rectangles(
    boundings: iamraw.BoundingBoxes,
    border: str = '1px solid black',
    background: str = 'transparent',
    more: str = '',
    reference: str = None,
    zindex: int = 10,
) -> str:
    """Render html rectangles represented as `<span>`."""
    collected = []
    for bounding in utila.xsome(boundings, count=4):
        rendered = render_rectangle(
            bounding=bounding,
            border=border,
            background=background,
            more=more,
            reference=reference,
            zindex=zindex,
        )
        collected.append(rendered)
    result = ''.join(collected)
    return result


LINE = """\
<svg {reference} style="position:absolute; top:{y0}px;left:{x0}px;
width:{width}px;height:{height}px;pointer-events: none; {more}" fill="none">
<line x1="1" y1="1" x2="{width}" y2="{height}" stroke="black"></line></svg>
"""


def render_line(
    bounding: iamraw.BoundingBox,
    more: str = '',
    reference: str = '',
) -> str:
    reference = html_reference(reference)
    bounding = utila.roundme(*bounding)  # reduce digits in html output
    x0, y0, x1, y1 = bounding
    assert y0 <= y1, str(bounding)
    assert x0 <= x1, str(bounding)
    height = y1 - y0
    width = x1 - x0
    height = max([height, 1])
    width = max([width, 1])
    rendered = LINE.format(
        height=height,
        more=more,
        reference=reference,
        width=width,
        x0=x0,
        y0=y0,
    )
    return rendered


HORIZONTAL = """\
<hr {reference} style="position:absolute;top:{y0}px;left:{x0}px;width:{width}px;"/>
"""


def render_horizontal(x0, y0, width, reference='') -> str:
    reference = html_reference(reference)
    rendered = HORIZONTAL.format(
        reference=reference,
        width=width,
        x0=x0,
        y0=y0,
    )
    return rendered


def html_reference(reference: str) -> str:
    if not reference or not reference.strip():
        return ''
    return f'id="{reference}" '
