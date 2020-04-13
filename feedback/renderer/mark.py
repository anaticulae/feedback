# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Mark the content
================

Separate TextMark, PageMark etc?

ater we need ImageMark, TableMark, DiagramMark

.. code-block:: none

    class Mark:
        page: int
        start: int
        end: int

    Marks = typing.List[Mark]

    class WordMark:
        page: int
        word: int = 23

    class SentenceMark:
        page: int
        sentence: 10

    class CharMark:
        page:int
        char: 1336

    class Marker:
        pages: range/int

    class PageMark:
        page: int
        start: int
        end: int


    def sentence(number=10,page=13):
        return Mark(page=13, start=133, end=155)

"""

import contextlib
import dataclasses
import glob
import typing

import protocol
import utila

import feedback.renderer.content
import feedback.utils.multiple_styles


@dataclasses.dataclass
class TextMark:
    page: int = None
    start: int = None
    end: int = None


TextMarks = typing.List[TextMark]


class WordAccess:

    def __init__(self, content: feedback.renderer.content.HTMLPageContents):
        self.content = {item.page: item for item in content}
        self.cache = {}

    def words(self, page):
        with contextlib.suppress(KeyError):
            return self.cache[page]

        result = []
        for container in self.content[page].content:
            for line in container:
                result.extend(line.text.strip().split())
        self.cache[page] = result
        return result

    def word(self, number, page):
        return self.words(page)[number]

    def length(self, page):
        return len(self.words(page))


@dataclasses.dataclass
class PageMarkConfiguration:
    page: int = None
    wordmarks: set = dataclasses.field(default_factory=set)
    linemarks: set = dataclasses.field(default_factory=set)


PageMarkConfigurations = typing.List[PageMarkConfiguration]


def create_configuration(marks: dict, page: int) -> PageMarkConfiguration:
    """Filter `marks` for selected `page`. Group them by word, line etc.

    Args:
        marks(int): dictonary with a list of marks per page
        page(int): selected page to return filtered marks
    Returns:
        generated PageMarkConfiguration
    """
    try:
        pagemarks = marks[page]
    except KeyError:
        pagemarks = {}
    wordmarks = protocol.words(pagemarks)
    linemarks = protocol.lines(pagemarks)

    result = PageMarkConfiguration(
        page=page,
        wordmarks=wordmarks,
        linemarks=linemarks,
    )
    return result


class WordMarker:
    """The word marker is used to mark selected words with an unique id
    to define the style in an external stylesheet later. This is used to
    hightlight important word and or to mark some failures due linter
    view.

    The **WordMarker** works on a single page and must be used within
    the page content from top to bottom. Resetting the word number is
    not possible.
    """

    def __init__(self, page, marks=None):
        """Initialize single WordMarker.

        Args:
            page(int): pagenumber of page to mark
            marks(set): set of number of words which must be highlighted
        """
        if marks is None:
            marks = set()
        self.marks = marks
        self.page = page
        self.index = 0

    def markme(self, line: str) -> feedback.utils.multiple_styles.Styles:
        """Add marker of defined `self.marks` words. Add for selected
        word with <span id="word{page}_{index}">word</span>.

        Args:
            line(str): line which can contain words
        Returns:
            `line` with marked words
        """
        # TODO: USE SENTENCE ALGO TO SPLIT WORDS?
        result = []
        current = ''
        for index, char in enumerate(line):
            if char == ' ':
                if current.strip():
                    result.append(self.decide_mark(current, index))
                    current = ''
            else:
                current = current + char
        if current:
            result.append(self.decide_mark(current, len(line)))
        result = [item for item in result if item]
        return result

    def decide_mark(self, item, endpos) -> feedback.utils.multiple_styles.Style:
        if not item.strip():
            # add only white spaces
            return None
        if self.index not in self.marks:
            self.index += 1
            return None
        startpos = endpos - len(item)
        result = feedback.utils.multiple_styles.Style(
            startpos,
            endpos,
            f'<span id="word{self.page}_{self.index}">',
            '</span>',
        )
        self.index += 1
        return result


class LineMarker:

    def __init__(self, page, marks=None):
        if marks is None:
            marks = set()
        self.marks = marks
        self.page = page
        self.index = 0

    def markme(self, line) -> feedback.utils.multiple_styles.Style:
        if not line:
            # white space line
            return None
        if not self.index in self.marks:
            self.index += 1
            return None
        start = f'<span id="line{self.page}_{self.index}">'
        end = '</span>'
        result = feedback.utils.multiple_styles.Style(0, len(line), start, end)
        self.index += 1
        return result


def collect(path: str) -> dict:
    """Collect marks from `path` and sort them by page."""
    with utila.chdir(path):
        findings = [
            protocol.load_result(item) for item in glob.glob('*_user.yaml')
        ]
    findings = utila.flatten(findings)
    result = protocol.bypage(findings)
    return result
