# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import typing

import protocol
import serializeraw
import utila
import words.feature.word

import feedback.problems
import feedback.templates


@utila.checkdatatype
def work(
        sections: str,
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
        pagenumbers: str,
        userlinting: str,
        pages: tuple = None,
) -> str:
    """Render problem view."""
    sections, text, headlines, lists, boxed, pagenumbers, problems = prepare_input(
        boxed=boxed,
        headlines=headlines,
        lists=lists,
        pagenumbers=pagenumbers,
        sections=sections,
        text=text,
        userlinting=userlinting,
        pages=pages,
    )
    result = process_content(
        boxed=boxed,
        headlines=headlines,
        listslookup=lists,
        pagenumbers=pagenumbers,
        problems=problems,
        sections=sections,
        text=text,
    )
    return result


def render_html(pages, problems) -> str:
    report = feedback.templates.template('problems', 'index.html')
    rendered = report.render(pages=pages, problems=problems)

    main_js = feedback.templates.template('problems', 'main.js').render()
    style_css = feedback.templates.template('problems', 'style.css').render()

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
        boxed,
        headlines,  # pylint:disable=W0613
        listslookup,
        pagenumbers: 'PageNumbersLookup',
        problems: dict,
        sections,
        text,
):
    # boxlookup = BoxLookUp(boxed)
    result = []
    for section in sections:
        for page in section:
            rendered = build_page(page, text, listslookup, boxed, pagenumbers)
            result.append(rendered)
    # update page number in pdf
    for index, item in enumerate(result):
        item.page = index
    rendered = render_html(result, problems)
    return rendered


def build_page(
        page,
        text,
        listslookup,
        boxed,
        pagenumbers,
) -> 'SinglePage':
    """Create data structure which is passed to Jinja to render the html
    output.

    Supported elements:
        headlines
        text
        boxes
        list
    """
    content = []
    with contextlib.suppress(KeyError):
        content = text[page.start]
        content = [
            prepare_headlinecontent(item, listslookup, boxed)
            for item in content
        ]
        content = utila.flatten(content)
    footer = None
    pdfpage = pagenumbers.userpage(page.start)
    if pdfpage is not None:
        footer = FooterHeader(userpage=pdfpage, hrline=True)
    # prepare
    result = SinglePage(
        width=800,
        height=700,
        content=content,
        footer=footer,
    )
    return result


@utila.checkdatatype
def prepare_input(
        boxed: str,
        headlines: str,
        lists: str,
        pagenumbers: str,
        sections: str,
        text: str,
        userlinting: str,
        pages: tuple = None,
):
    sections = serializeraw.load_sections(sections, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines, pages=pages)

    loaded = serializeraw.load_lists(lists, pages=pages)
    listlookup = words.feature.word.ListLookUp(loaded)

    boxed = serializeraw.load_boxedcontent(boxed, pages=pages)
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers, pages=pages)
    pagenumbers = PageNumbersLookup(pagenumbers)

    result: typing.List[protocol.Finding] = protocol.load_result(userlinting)
    problems = protocol.bypage(result)

    text = {item[0]: item[1] for item in text}
    return sections, text, headlines, listlookup, boxed, pagenumbers, problems


class PageNumbersLookup:

    def __init__(self, pagenumbers):
        loader = (PageNumbersLookup._prepare_double if isinstance(
            pagenumbers, tuple) else PageNumbersLookup._prepare_single)
        self.data = loader(pagenumbers)

    def userpage(self, pdfpage: int):
        with contextlib.suppress(KeyError):
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


@dataclasses.dataclass
class FooterHeader:
    userpage: str = ''
    hrline: bool = False
    height: int = 30


@dataclasses.dataclass
class SinglePage:
    width: int = -1
    height: int = -1
    content: str = ''
    footer: FooterHeader = None
    page: int = -1


def prepare_headlinecontent(  # pylint:disable=R1260,R0914
        paragraph,
        listlookup: words.feature.word.ListLookUp,
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
    box_open = NO_BOXED
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
            if not listitem:
                continue
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
            # TODO: SEEMS TO BE A BUG. CONVERTING MUST NOT BE REQUIRED
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
    content = content.replace(utila.NEWLINE, '<br />')
    return content


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

NO_BOXED = -1
BOXED_START = 0


def find_list(listlookup, page, item, index):
    lists = listlookup.data[page]
    for content, _index in lists:
        if _index != item:
            continue
        try:
            return content[2].data[index]
        except IndexError:
            utila.error(f'could not find list item: {page} {item} {index}')
    return None


def find_boxed(boxedlookup, page, item, boxindex):
    # TODO: Bad solution!
    boxedlookup = {page: content for page, content in boxedlookup}
    try:
        content = boxedlookup[page]
    except IndexError:
        return None
    for (_, __, boxedcontent) in content:
        # match
        for boxes in boxedcontent:
            for (_, (index, content)) in boxes:
                if index != item:
                    continue
                try:
                    return content[boxindex][2]
                except IndexError:
                    return item
    return None


def name() -> str:
    return feedback.cli.FEATURE_NAME
