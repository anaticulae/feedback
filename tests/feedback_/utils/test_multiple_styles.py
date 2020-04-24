# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.utils.multiple_styles as fums


def test_merge():
    msg = 'Hier!Spricht Helm'
    first = fums.Style(0, 5, '<bat>', '</bat>')
    second = fums.Style(4, 10, '<cat>', '</cat>')

    styles = [first, second]
    result = fums.merger(msg, styles)
    expected = '<bat>Hier</bat><bat><cat>!</cat></bat><cat>Spric</cat>ht Helm'
    assert result == expected, str(result)


def test_merge_raw():
    msg = 'Hier Spricht Helm'
    raw = fums.create_raw(msg)
    merged = fums.tostring(msg, [raw])
    assert merged == msg, merged


def test_merge_two_styles():
    first = fums.Style(0, 5, '<bat>', '</bat>')
    second = fums.Style(4, 10, '<cat>', '</cat>')

    merged = fums.merge_two(first, second)
    # yapf:disable
    expected = [
        fums.Style(start=0, end=4, first='<bat>', last='</bat>'),
        fums.Style(start=4, end=5, first='<bat>{*}<cat>', last='</bat>{*}</cat>'),
        fums.Style(start=5, end=10, first='<cat>', last='</cat>'),
    ]
    # yapf:enable
    assert merged == expected
