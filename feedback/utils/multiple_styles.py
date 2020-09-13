# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import operator
import typing

import utila

Style = collections.namedtuple('Style', 'start, end, first, last')
Styles = typing.List[Style]

STYLE_SEPARATOR = '{*}'


def merger(text: str, styles: Styles) -> str:
    validate_range(styles, len(text))
    # determine max length if defined style is longer than given text
    # TODO: ADD LOG INFO?
    length = utila.maxs([item.end for item in styles], len(text))
    merged = [create_raw(' ' * length)]

    styles = sort_style(styles)
    styles = simplify(styles)
    styles = sort_style(styles)  # TODO: HACK?

    for style in styles:
        merged = merge(merged, style)

    result = tostring(text, merged)
    return result


def simplify(items):
    """\
    >>> simplify([Style(start=0, end=5, first='ABC', last='/ABC'),
    ... Style(start=5, end=10, first='ABC', last='/ABC')])
    [Style(start=0, end=10, first='ABC', last='/ABC')]
    """
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        before = result[-1]
        if before.end != item.start or before.first != item.first or before.last != item.last:
            result.append(item)
        else:
            # unite style
            # before.end = item.end
            replaced = before._replace(end=item.end)  # pylint:disable=W0212
            result[-1] = replaced
    return result


def validate_range(styles, length):  # pylint:disable=W0613
    for item in styles:
        assert item.start <= item.end, str(item)
        # TODO: ENABLE LATER
        # assert item.end <= length, f'{length}: {item}'


def sort_style(items):
    """Sort by `start` index and `end` reversed."""
    items = sorted(items, key=operator.itemgetter(1), reverse=True)
    items = sorted(items, key=operator.itemgetter(0))
    return items


def merge(items, current):
    result = sort_style(items)
    candiate = should_split(result, current)
    if len(candiate) == 1:
        merged = merge_two(*sort_style([candiate[0], current]))
        result.remove(candiate[0])
        result.extend(merged)
    elif len(candiate) == 2:
        merged = merge_three(candiate[0], current, candiate[1])
        result.remove(candiate[0])
        result.remove(candiate[1])
        result.extend(merged)
    else:
        assert not candiate, candiate
        result.append(current)
    result = sort_style(result)
    return result


def merge_two(first, second):
    """Merge two style in a common pattern. It is possible to build one,
    two or three resulting pattern.

    >>> merge_two(Style(0,5,'<h1>','</h1>'), Style(0,5,'<b>','</b>'))
    [Style(start=0, end=5, first='<h1>{*}<b>', last='</h1>{*}</b>')]
    >>> merge_two(Style(0,5,'<bat>','</bat>'), Style(4,5,'<cat>','</cat>')) # doctest: +NORMALIZE_WHITESPACE
    [Style(start=0, end=4, first='<bat>', last='</bat>'),\
         Style(start=4, end=5, first='<bat>{*}<cat>', last='</bat>{*}</cat>')]
    >>> merge_two(Style(0,5,'<h1>','</h1>'), Style(3,10,'<b>','</b>')) # doctest: +NORMALIZE_WHITESPACE
    [Style(start=0, end=3, first='<h1>', last='</h1>'), \
    Style(start=3, end=5, first='<h1>{*}<b>', last='</h1>{*}</b>'), \
    Style(start=5, end=10, first='<b>', last='</b>')]
    """
    first_new = (first.start, min([first.end, second.start]))
    second_new = (max([first.end, second.start]), second.end)
    middle_new = first_new[1], second_new[0]

    if first.end > second.end:
        # first overlaps seconds
        first_new = first.start, second.start
        middle_new = second.start, second.end
        second_new = second.end, first.end

    middle_merged_style_first = first.first
    if second.first:
        if first.first:
            middle_merged_style_first = first.first + STYLE_SEPARATOR + second.first
        else:
            middle_merged_style_first = second.first

    middle_merged_style_last = first.last
    if second.last:
        if first.last:
            middle_merged_style_last = first.last + STYLE_SEPARATOR + second.last
        else:
            middle_merged_style_last = second.last

    middle = Style(
        *middle_new,
        middle_merged_style_first,
        middle_merged_style_last,
    )
    if first.end > second.end:
        second = Style(
            *second_new,
            first.first,
            first.last,
        )
    else:
        second = Style(
            *second_new,
            second.first,
            second.last,
        )
    first = Style(
        *first_new,
        first.first,
        first.last,
    )
    result = []
    if first[0] != first[1]:
        result.append(first)
    if middle[0] != middle[1]:
        result.append(middle)
    if second[0] != second[1]:
        result.append(second)
    return result


def merge_three(left, middle, right):
    left, middle, right = sort_style((left, middle, right))
    result = []
    result.extend(merge_two(left, middle))
    result.extend(merge_two(middle, right))
    result = make_unique(result)
    return result


def make_unique(items):
    items = utila.make_unique(items)
    # item is included in other group
    remove = [[
        index for index, check in enumerate(items) if all((
            check.start == item.start,
            check.end == item.end,
            item.first in check.first,
            item.last in check.last,
        ))
    ] for item in items]
    # remove redundant items
    items = [
        item for item, selected in zip(items, remove) if len(selected) == 1
    ]
    return items


def should_split(items, current):
    result = []
    if current is None:
        return result
    for item in items:
        if any((
                item.start < current.start < item.end,
                item.start < current.end < item.end,
        )):
            result.append(item)
        elif item.start == current.start and item.end == current.end:
            result.append(item)
    return result


def create_raw(text: str):
    return Style(0, len(text), '', '')


def tostring(raw: str, items: Styles) -> str:
    """Merge style decorator into `raw` text.

    >>> tostring('Helm hier', [Style(0,4,'<h1>','</h1>'), Style(4,9,'','')])
    '<h1>Helm</h1> hier'
    >>> tostring('Helm hier', [Style(0,4,'<h1>{*}<b>','</h1>{*}</b>'), Style(4,9,'','')])
    '<h1><b>Helm</b></h1> hier'
    """
    merged = ''
    for item in items:
        chunk = raw[item.start:item.end]
        if item.first:
            # <tag1><tag2>chunk</tag2></tag1>
            starting = ''.join(item.first.split('{*}'))
            # reverse to ensure that tags does not overlap
            ending = ''.join(reversed(item.last.split('{*}')))
            if not chunk:
                # skip empty, style without content
                # TODO: THIS IS A HINT FOR WRONG STYLING?
                continue
            merged += f'{starting}{chunk}{ending}'
        else:
            # raw chunk
            merged += chunk
    return merged
