# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import feedback.renderer.mark
from tests.feedback.fixtures import masterpage72  # pylint:disable=W0611


def test_renderer_mark_access_words(masterpage72):  # pylint:disable=W0621
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


def test_renderer_mark_word_marker_whitespace():
    """Ensure to skip marking white spaces."""
    marks = set([3, 4, 5, 7, 11])
    marker = feedback.renderer.mark.WordMarker(page=2, marks=marks)
    for _ in range(20):
        marked = marker.markme('  ')
        assert '<span' not in marked, marked
        marked = marker.markme(' ')
        assert '<span' not in marked, marked


def test_renderer_mark_line_marker():
    marker = feedback.renderer.mark.LineMarker(page=1, marks=set([1, 2]))
    assert marker.markme('first line') == 'first line'

    expected = '<span id="line1_1">second line</span>'
    assert marker.markme('second line') == expected

    expected = '<span id="line1_2">third line</span>'
    assert marker.markme('third line') == expected

    expected = 'fourth line'
    assert marker.markme('fourth line') == expected


def test_render_mark_filter_lines():
    create_line = protocol.Location.from_oneline
    create_chapter = protocol.Location.from_chapter
    findings = [
        protocol.Finding(location=create_chapter(chapter=3, page=3)),
        protocol.Finding(location=create_chapter(chapter=4, page=3)),
        protocol.Finding(location=create_chapter(chapter=5, page=3)),
        protocol.Finding(location=create_line(line=5, page=3)),
        protocol.Finding(location=create_line(line=7, page=3)),
        protocol.Finding(location=create_line(line=10, page=3)),
        protocol.Finding(location=create_chapter(chapter=1, page=3)),
    ]
    filtered = feedback.renderer.mark.lines(findings)
    assert len(filtered) == 3, str(filtered)


def test_render_mark_filter_words():
    create_line = protocol.Location.from_oneline
    create_chapter = protocol.Location.from_chapter
    findings = [
        protocol.Finding(location=create_chapter(chapter=3, page=3)),
        protocol.Finding(location=create_chapter(chapter=5, page=3)),
        protocol.Finding(location=protocol.Location.fromstr('w30p3')),
        protocol.Finding(location=protocol.Location.fromstr('w130p3')),
        protocol.Finding(location=protocol.Location.fromstr('w5p3')),
        protocol.Finding(location=protocol.Location.fromstr('w0p3')),
        protocol.Finding(location=create_line(line=7, page=3)),
        protocol.Finding(location=create_chapter(chapter=1, page=3)),
    ]
    filtered = feedback.renderer.mark.words(findings)
    assert len(filtered) == 4, str(filtered)
