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
import typing

import german
import protocol
import utila

import feedback.renderer.content
import feedback.utils.multiple_styles as fums


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
        for container in self.content[page].navigator:
            for line in container.text.splitlines():
                result.extend(line.strip().split())
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
    linemarks: dict = dataclasses.field(default_factory=dict)


PageMarkConfigurations = typing.List[PageMarkConfiguration]

COMPLETE_LINE = None


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
    # require selected word only, reason etc. is not important here
    wordmarks = [item.location.value for item in wordmarks]
    linemarks = protocol.lines(pagemarks)
    ranges = ranged(pagemarks)

    lines = {}
    for item in linemarks:
        lines[item.location.value] = COMPLETE_LINE
    for item in ranges:
        # TODO: SUPPORT MULTILINE
        start, end = item.location.line, item.location.line_end
        # TODO: CHANGE TO CHAR
        charstart, charend = item.location.token, item.location.token_end
        if end is None:
            end = start
        # TODO: REPLACE WITH UTILA CODE
        for number in utila.ranged_tuple(start, end + 1):
            if charstart is None:
                lines[number] = COMPLETE_LINE
            else:
                # TODO: CHECK FOR MULTILINE ENVIRONMENT
                # TODO-CONCEPT: charstart in first line, middle lines complete,
                # charend for last line.
                lines[number] = (charstart, charend)
    result = PageMarkConfiguration(
        page=page,
        wordmarks=wordmarks,
        linemarks=lines,
    )
    return result


def ranged(items: protocol.Findings) -> protocol.Findings:
    # TODO: REPLACE WITH PROTOCOL CODE
    return protocol.filter_mark(items, shortcut='r')


class WordGenerator:

    def __init__(self):
        self.index = 0

    def words(self, line):
        splitted = german.split_token(line, normalize=False)
        for item in splitted:
            if not item or not item.strip():
                continue
            yield self.index, item
            self.index += 1


def best_sync(left, right) -> utila.Numbers:
    result = []
    rightlength = len(right)
    rightside = set(right)
    for index in range(len(left)):
        leftside = set(left[index:index + rightlength])
        common = len(rightside & leftside)
        result.append(common)
    max_equal = max(result)
    try:
        start = result.index(max_equal)
    except ValueError:
        return None
    words = [item for item in range(start, start + rightlength)]
    return words


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

    def markme(self, line: str) -> fums.Styles:
        """Add marker of defined `self.marks` words. Add for selected
        word with <span id="word{page}_{index}">word</span>.

        Args:
            line(str): line which can contain words
        Returns:
            `line` with marked words
        """
        result = []
        startpos = 0
        splitted = german.split_token(line, normalize=False)
        for word in splitted:
            result.append(self.decide_mark(word, startpos))
            # TODO: ADD OPTION TO INCLUDE WHITESPACE INTO WORD
            startpos += len(word) + 1  # +1 for whitespace
        result = [item for item in result if item]
        return result

    def decide_mark(self, item, startpos) -> fums.Style:
        if not item.strip():
            # add only white spaces
            return None
        if self.index not in self.marks:
            self.index += 1
            return None
        endpos = startpos + len(item)
        result = fums.Style(
            startpos,
            endpos,
            f'<span id="word{self.page}_{self.index}">',
            '</span>',
        )
        self.index += 1
        return result


class LineMarker:

    def __init__(self, page, marks: dict = None, startofcontent: int = None):
        self.page = page
        self.index = 0 if startofcontent is None else 0 - startofcontent
        if isinstance(marks, dict):
            self.marks = marks
        elif isinstance(marks, (set, list)):
            # take complete line
            self.marks = {item: None for item in set(marks)}
        else:
            self.marks = dict()

    def markme(self, line: str) -> fums.Style:
        if not line:
            # white space line
            return None
        if not self.index in self.marks:
            self.index += 1
            return None
        start = f'<span id="line{self.page}_{self.index}">'
        end = '</span>'
        try:
            # check if added marks contains char start and char end
            charstart, charend = self.marks[self.index]
        except (KeyError, TypeError):
            # no additional styling information available, use whole line
            charstart, charend = 0, len(line)
        result = fums.Style(charstart, charend, start, end)
        self.index += 1
        return result
