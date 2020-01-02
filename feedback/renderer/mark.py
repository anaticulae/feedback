# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Separate TextMark, PageMark etc?

ater we need ImageMark, TableMark, DiagramMark

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

import feedback.problems.linter
import feedback.renderer.html


@dataclasses.dataclass
class TextMark:
    page: int = None
    start: int = None
    end: int = None


TextMarks = typing.List[TextMark]


class WordAccess:

    def __init__(self, content: feedback.renderer.HTMLPageContents):
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
    wordmarks = words(pagemarks)
    linemarks = lines(pagemarks)

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

    def markme(self, line: str) -> str:
        """Add marker of defined `self.marks` words. Add for selected
        word with <span id="word{page}_{index}">word</span>.

        Args:
            line(str): line which can contain words
        Returns:
            `line` with marked words
        """
        result = []
        current = ''
        for char in line:
            if char == ' ':
                if current.strip():
                    result.append(self.decide_mark(current))
                    result.append(' ')
                    current = ''
                else:
                    result.append(char)
            else:
                current = current + char
        if current:
            result.append(self.decide_mark(current))
        return ''.join(result)

    def decide_mark(self, item):
        if not item.strip():
            # add only white spaces
            return item
        if self.index not in self.marks:
            self.index += 1
            return item
        result = f'<span id="word{self.page}_{self.index}">{item}</span>'
        self.index += 1
        return result


class LineMarker:

    def __init__(self, page, marks=None):
        if marks is None:
            marks = set()
        self.marks = marks
        self.page = page
        self.index = 0

    def markme(self, line) -> str:
        if not line.strip():
            # white space line
            return line
        if not self.index in self.marks:
            self.index += 1
            return line
        result = f'<span id="line{self.page}_{self.index}">{line}</span>'
        self.index += 1
        return result


def collect(path: str) -> dict:
    """Collect marks from `path` and sort them by page."""
    with utila.chdir(path):
        findings = [
            protocol.load_result(item) for item in glob.glob('*_user.yaml')
        ]
    result = feedback.problems.linter.group_finding_bypage(findings)
    return result


# TODO: MOVE TO PROTOCOL PACKAGE
def words(items: protocol.Findings) -> protocol.Findings:
    return filter_mark(items, 'w')


def lines(items: protocol.Findings) -> protocol.Findings:
    return filter_mark(items, 'ol')


def filter_mark(items: protocol.Findings, shortcut: str) -> protocol.Findings:
    """Filter `Findings` by shortcut and sort them by `location.value`
    afterwards.

    Args:
        items(protocol.Findings): list of findings
        shortcut(str): shortcut of finding.location, w word, p page,
                       ol oneline, etc.
    Returns:
        filtered, sorted list of `Findings`
    """
    assert all([item.location for item in items]), f'require location: {items}'
    items = [item for item in items if item.location.shortcut == shortcut]
    items = sorted(items, key=lambda x: x.location.value)
    return items
