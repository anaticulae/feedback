# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol

import feedback.renderer.mark
import feedback.utils.multiple_styles


def test_renderer_mark_access_words(masterpage72):
    access = feedback.renderer.mark.WordAccess(masterpage72)
    assert access.word(12, 0) == 'Studiengang:'


def test_renderer_mark_word_marker():
    marks = {3, 4, 5, 7, 11}
    marker = feedback.renderer.mark.WordMarker(page=2, marks=marks)

    line = '  Hier spricht super Helmut. Wie gehts    es dir mein Freund?    '
    # yapf:disable
    expected = [
        feedback.utils.multiple_styles.Style(19, 26, '<span id="word2_3">', '</span>'),
        feedback.utils.multiple_styles.Style(27, 30, '<span id="word2_4">', '</span>'),
        feedback.utils.multiple_styles.Style(31, 36, '<span id="word2_5">', '</span>'),
        feedback.utils.multiple_styles.Style(40, 43, '<span id="word2_7">', '</span>'),
    ]
    # yapf:enable
    result = marker.markme(line)
    assert result == expected

    # yapf:disable
    last = [
        feedback.utils.multiple_styles.Style(6, 8, '<span id="word2_11">', '</span>'),
    ]
    # yapf:enable
    string = 'hello mr tom'
    result = marker.markme(string)
    assert result == last
    assert string[last[0].start:last[0].end] == 'mr'


def test_renderer_mark_word_marker_whitespace():
    """Ensure to skip marking white spaces."""
    marks = set([3, 4, 5, 7, 11])
    marker = feedback.renderer.mark.WordMarker(page=2, marks=marks)
    for _ in range(20):
        marked = marker.markme('  ')
        assert not marked, marked


def test_renderer_mark_line_marker():
    marker = feedback.renderer.mark.LineMarker(page=1, marks=set([1, 2]))
    assert marker.markme('first line') is None

    expected = feedback.utils.multiple_styles.Style(
        start=0,
        end=len('second line'),
        first='<span id="line1_1">',
        last='</span>',
    )
    assert marker.markme('second line') == expected

    expected = feedback.utils.multiple_styles.Style(
        start=0,
        end=len('third line'),
        first='<span id="line1_2">',
        last='</span>',
    )
    assert marker.markme('third line') == expected

    assert marker.markme('fourth line') is None


def test_render_mark_filter_lines():
    create_line = iamraw.Location.from_oneline
    create_chapter = iamraw.Location.from_chapter
    findings = [
        iamraw.Finding(location=create_chapter(chapter=3, page=3)),
        iamraw.Finding(location=create_chapter(chapter=4, page=3)),
        iamraw.Finding(location=create_chapter(chapter=5, page=3)),
        iamraw.Finding(location=create_line(line=5, page=3)),
        iamraw.Finding(location=create_line(line=7, page=3)),
        iamraw.Finding(location=create_line(line=10, page=3)),
        iamraw.Finding(location=create_chapter(chapter=1, page=3)),
    ]
    filtered = protocol.lines(findings)
    assert len(filtered) == 3, str(filtered)


def test_render_mark_filter_words():
    create_line = iamraw.Location.from_oneline
    create_chapter = iamraw.Location.from_chapter
    findings = [
        iamraw.Finding(location=create_chapter(chapter=3, page=3)),
        iamraw.Finding(location=create_chapter(chapter=5, page=3)),
        iamraw.Finding(location=iamraw.Location.fromstr('w30p3')),
        iamraw.Finding(location=iamraw.Location.fromstr('w130p3')),
        iamraw.Finding(location=iamraw.Location.fromstr('w5p3')),
        iamraw.Finding(location=iamraw.Location.fromstr('w0p3')),
        iamraw.Finding(location=create_line(line=7, page=3)),
        iamraw.Finding(location=create_chapter(chapter=1, page=3)),
    ]
    filtered = protocol.words(findings)
    assert len(filtered) == 4, str(filtered)
