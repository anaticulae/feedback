# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from contextlib import suppress
from dataclasses import dataclass

from jinja2 import PackageLoader
from jinja2 import Template
from serializeraw import load_boxedcontent
from serializeraw import load_headlines
from serializeraw import load_lists
from serializeraw import load_sections
from serializeraw import load_text
from utila import NEWLINE
from utila import Flag
from utila import checkdatatype
from utila import flatten
from words.feature.words import ListLookUp


@checkdatatype
def work(
        sections: str,
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
) -> str:
    sections, text, headlines, lists, boxed = prepare_input(
        sections,
        text,
        headlines,
        lists,
        boxed,
    )

    result = process_content(
        sections,
        text,
        headlines,
        lists,
        boxed,
    )

    return result


@checkdatatype
def prepare_input(
        sections: str,
        text: str,
        headlines: str,
        lists: str,
        boxed: str,
):
    sections = load_sections(sections)
    headlines = load_headlines(headlines)
    text = load_text(text, headlines)
    lists = load_lists(lists)
    boxed = load_boxedcontent(boxed)

    text = {item[0]: item[1] for item in text}
    return sections, text, headlines, lists, boxed


@dataclass
class SinglePage:
    width: int = -1
    height: int = -1
    content: str = ''


def process_content(
        sections,
        text,
        headlines,
        lists,
        boxed,
):
    # for key, value in text.items():
    #     print(key)
    #     print(value)
    #     print()
    #     print()
    listlookup = ListLookUp(lists)
    # boxlookup = BoxLookUp(boxed)
    result = []
    for section in sections:
        for page in section:
            content = ['Page %d' % page.start]
            with suppress(KeyError):
                content = text[page.start]
                content = [
                    prepare_headlinecontent(item, listlookup, boxed)
                    for item in content
                ]
                content = flatten(content)

            # prepare
            content = SinglePage(width=800, height=700, content=content)
            # for item in page:
            #     print(item)
            result.append(content)
    rendered = render(result)
    return rendered


# TODO: Define `hey`/ general public API?

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


def prepare_headlinecontent(
        paragraph,
        listlookup: ListLookUp,
        boxed,
):
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


def render(pages) -> str:
    loader = PackageLoader('feedback.report')
    reporttemplate = Template(loader.get_source(None, 'report.html')[0])
    rendered = reporttemplate.render(pages=pages)
    return rendered


def name():
    return 'view'


def commandline():
    return Flag(longcut=name(), message='export the html result of %s' % name())


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
