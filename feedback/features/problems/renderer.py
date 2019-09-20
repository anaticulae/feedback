# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import typing
from contextlib import suppress
from dataclasses import dataclass

import protocol
from jinja2 import PackageLoader
from jinja2 import Template
from serializeraw import load_boxedcontent
from serializeraw import load_headlines
from serializeraw import load_lists
from serializeraw import load_pagenumbers
from serializeraw import load_sections
from serializeraw import load_text
from utila import NEWLINE
from utila import checkdatatype
from utila import flatten
from words.feature.words import ListLookUp

import feedback.problems


@checkdatatype
def work(
        sections: str,
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
        pagenumbers: str,
        userlinting: str,
) -> str:
    sections, text, headlines, lists, boxed, pagenumbers, problems = prepare_input(
        sections,
        text,
        headlines,
        lists,
        boxed,
        pagenumbers,
        userlinting,
    )

    result = process_content(
        sections,
        text,
        headlines,
        lists,
        boxed,
        pagenumbers,
        problems,
    )

    return result


def render(pages, problems) -> str:
    # TODO: improve with more jinja appraoch
    loader = PackageLoader('feedback.features.problems')
    reporttemplate = Template(loader.get_source(None, 'index.html')[0])
    rendered = reporttemplate.render(pages=pages, problems=problems)

    main_js = loader.get_source(None, 'main.js')[0]
    style_css = loader.get_source(None, 'style.css')[0]

    result = f"""
    <style>
    {style_css}
    </style>
    <script>
    {main_js}
    </script>
    {rendered}
    """
    return result


def process_content(
        sections,
        text,
        headlines,
        listslookup,
        boxed,
        pagenumbers: 'PageNumbersLookup',
        problems: dict,
):
    # boxlookup = BoxLookUp(boxed)
    result = []
    for section in sections:
        for page in section:
            content = []
            with suppress(KeyError):
                content = text[page.start]
                content = [
                    prepare_headlinecontent(item, listslookup, boxed)
                    for item in content
                ]
                content = flatten(content)
            footer = None
            pdfpage = pagenumbers.userpage(page.start)
            if pdfpage is not None:
                footer = FooterHeader(userpage=pdfpage, hrline=True)
            # prepare
            content = SinglePage(
                width=800,
                height=700,
                content=content,
                footer=footer,
            )

            result.append(content)
    # update page number in pdf
    for index, item in enumerate(result):
        item.page = index
    rendered = render(result, problems)
    return rendered


@checkdatatype
def prepare_input(
        sections: str,
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
        pagenumbers: str,
        userlinting: str,
):
    sections = load_sections(sections)
    headlines = load_headlines(headlines)
    text = load_text(text, headlines)

    lists = load_lists(lists)
    lists = ListLookUp(lists)

    boxed = load_boxedcontent(boxed)
    pagenumbers = load_pagenumbers(pagenumbers)
    pagenumbers = PageNumbersLookup(pagenumbers)

    result: typing.List[protocol.Finding] = protocol.load_result(userlinting)
    problems = feedback.problems.linter.group_finding_bypage(result)

    text = {item[0]: item[1] for item in text}

    return sections, text, headlines, lists, boxed, pagenumbers, problems


class PageNumbersLookup:

    def __init__(self, pagenumbers):
        loader = (PageNumbersLookup._prepare_double if isinstance(
            pagenumbers, tuple) else PageNumbersLookup._prepare_single)
        self.data = loader(pagenumbers)

    def userpage(self, pdfpage: int):
        with suppress(KeyError):
            return self.data[pdfpage]
        return None

    @staticmethod
    def _prepare_single(items):
        return {pdfpage: page for (pdfpage, _, page) in items}

    @staticmethod
    def _prepare_double(items):
        (left, right) = items
        left = PageNumbersLookup._prepare_single(left)
        right = PageNumbersLookup._prepare_single(right)

        for key, value in right.items():
            left[key] = value
        return left


@dataclass
class FooterHeader:
    userpage: str = ''
    hrline: bool = False
    height: int = 30


@dataclass
class SinglePage:
    width: int = -1
    height: int = -1
    content: str = ''
    footer: FooterHeader = None
    page: int = -1


# TODO: Define `hey`/ general public API?


def prepare_headlinecontent(
        paragraph,
        listlookup: ListLookUp,
        boxed,
) -> typing.List[str]:
    # TODO: Rework when jinja documentation is available
    headline, content = paragraph
    level = headline.level if headline.level is not None else 2
    page = headline.page
    if headline.text is not None:
        headline = '<h%d>%s</h%d>' % (level, headline.text, level)

    result = []
    list_open = NO_LIST
    box_open = NO_LIST
    # assert 0
    for item in content:
        listcontent = listindex(item) is not None
        if not listcontent and list_open > NO_LIST:
            # close list
            list_open = NO_LIST
            result.append('</ul>')
        if listcontent and list_open == NO_LIST:
            list_open = LIST_START
            result.append('<ul>')
        if listcontent:
            # listitem = listlookup.
            listitem = find_list(listlookup, page, listindex(item), list_open)
            _, listtext = listitem
            result.append('<li>%s</li>' % listtext)
            list_open += 1
            continue
        boxcontent = boxedcontentindex(item) is not None
        if not boxcontent and box_open > NO_BOXED:
            # close boxed
            box_open = NO_BOXED
            result.append('</div>')
        if boxcontent and box_open == NO_BOXED:
            box_open = BOXED_START
            result.append(
                '<div style="border: 1px solid #665544; padding:5px; margin:5px;">'
            )
        if box_open != NO_BOXED:
            # TODO: only print first item, we have to restructure boxed result
            boxedcontent = find_boxed(
                boxed,
                page,
                boxedcontentindex(item),
                box_open,
            )
            boxedcontent = escape_content(boxedcontent)
            result.append('%s<br/>' % boxedcontent)
            box_open += 1
            continue
        result.append('%s' % item)

    if box_open:
        result.append('</div>')
    if list_open:
        result.append('</ul>')

    if not isinstance(headline, str):
        return result
    return [headline] + result


def escape_content(content):
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    content = content.replace(NEWLINE, '<br />')
    return content


def preprare_boxcontent(item):
    pass


def prepare_listcontent(item):
    pass


def parseindex(item, checkedchar):
    try:
        index, char = int(item[0:-1]), item[-1]
    except ValueError:
        return None
    if not char == checkedchar:
        return None
    return index


def listindex(item):
    return parseindex(item, 'l')


def boxedcontentindex(item):
    return parseindex(item, 'b')


NO_LIST = -1
LIST_START = 0

BOXED_START = 0
NO_BOXED = -1


def find_list(listlookup, page, item, index):
    lists = listlookup.data[page]
    for content, _index in lists:
        if _index == item:
            return content[2].data[index]
    return None


def find_boxed(boxedlookup, page, item, boxindex):
    # TODO: Bad solution!
    # for item in boxedlookup:
    #     print(item)
    #     print()
    #     print()
    # assert 0
    for (current_page, content) in boxedlookup:
        if current_page != page:
            continue
        for (_, __, boxedcontent) in content:
            # match
            for www in boxedcontent:
                for (bounding, (index, content)) in www:
                    if index == item:
                        try:
                            return content[boxindex][2]
                        except IndexError:
                            return item
    return None


def name() -> str:
    return feedback.cli.FEATURE_NAME
