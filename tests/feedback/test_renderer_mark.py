# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.renderer.mark
from tests.feedback.fixtures import masterpage72  # pylint:disable=W0611


def test_renderer_mark_access_words(masterpage72):  # pylint:disable=W0621
    # firstpage = utila.select_page(masterpage72, 0)
    access = feedback.renderer.mark.WordAccess(masterpage72)
    assert access.word(12, 0) == 'Studiengang:'


def test_renderer_mark_word_marker():
    marks = set([3, 4, 5, 7, 11])
    marker = feedback.renderer.mark.WordMarker(page=2, marks=marks)

    line = '  Hier spricht super Helmut. Wie gehts    es dir mein Freund?    '
    expected = ('  Hier spricht super <span id="word2_3">Helmut.</span> '
                '<span id="word2_4">Wie</span> '
                '<span id="word2_5">gehts</span> '
                '   es <span id="word2_7">dir</span> mein Freund?    ')
    result = marker.markme(line)
    assert result == expected

    result = marker.markme('hello mr tom')
    assert result == 'hello <span id="word2_11">mr</span> tom'


def test_renderer_mark_line_marker():
    marker = feedback.renderer.mark.LineMarker(page=1, marks=set([1, 2]))
    assert marker.markme('first line') == 'first line'

    expected = '<span id="line1_1">second line</span>'
    assert marker.markme('second line') == expected

    expected = '<span id="line1_2">third line</span>'
    assert marker.markme('third line') == expected

    expected = 'fourth line'
    assert marker.markme('fourth line') == expected
