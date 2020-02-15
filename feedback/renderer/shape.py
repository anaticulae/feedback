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


# Rectangle - Item is moved to the background with z-index: -1000; let
# text selectable. If the index is not negative, the rectangle will hide
# the focus of the underlaying content.
RECTANGLE = """\
<span {reference} style="position:absolute;
top:{y0}px;left:{x0}px;width:{width}px;height:{height}px;
border:{border}; background:{background}; z-index: -1000;
{more}"></span>"""


def render_rectangle(
        bounding: iamraw.BoundingBox,
        border: str = '1px solid black',
        background: str = 'transparent',
        more: str = '',
        reference: str = None,
) -> str:
    """Render html rectangle represented as `<span>`."""
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
