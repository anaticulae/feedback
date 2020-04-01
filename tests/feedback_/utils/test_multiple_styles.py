# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.utils.multiple_styles


def test_merge():
    msg = 'Hier!Spricht Helm'
    first = feedback.utils.multiple_styles.Style(0, 5, '<bat>', '</bat>')
    second = feedback.utils.multiple_styles.Style(4, 10, '<cat>', '</cat>')

    styles = [first, second]
    result = feedback.utils.multiple_styles.merger(msg, styles)
    expected = '<bat>Hier</bat><bat><cat>!</cat></bat><cat>Spric</cat>ht Helm'
    assert result == expected, str(result)


def test_merge_raw():
    msg = 'Hier Spricht Helm'
    raw = feedback.utils.multiple_styles.create_raw(msg)
    merged = feedback.utils.multiple_styles.tostring(msg, [raw])
    assert merged == msg, merged


def test_merge_two_styles():
    first = feedback.utils.multiple_styles.Style(0, 5, '<bat>', '</bat>')
    second = feedback.utils.multiple_styles.Style(4, 10, '<cat>', '</cat>')

    merged = feedback.utils.multiple_styles.merge_two(first, second)
    expected = [
        feedback.utils.multiple_styles.Style(
            start=0, end=4, first='<bat>', last='</bat>'),
        feedback.utils.multiple_styles.Style(
            start=4, end=5, first='<bat>{*}<cat>', last='</bat>{*}</cat>'),
        feedback.utils.multiple_styles.Style(
            start=5, end=10, first='<cat>', last='</cat>'),
    ]
    assert merged == expected
