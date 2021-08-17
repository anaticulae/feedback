# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import iamraw
import iamraw.path
import iamraw.sections
import serializeraw
import texmex
import textflow.alignment.style
import textflow.features.alignment
import textflow.path
import textflow.serialize
import utila

import feedback.renderer.boxes
import feedback.renderer.content
import feedback.renderer.images
import feedback.renderer.mark
import feedback.renderer.shape
import feedback.renderer.text
import feedback.utils.multiple_styles


def load(  # pylint:disable=R0914,too-many-arguments
    text: str,
    textposition: str,
    oneline_text: str,
    oneline_textposition: str,
    borders: str,
    alignment: str = None,
    boxes: str = None,
    fontheader: str = None,
    fontcontent: str = None,
    oneline_fontheader: str = None,
    oneline_fontcontent: str = None,
    hits: str = None,
    horizontals: str = None,
    images: str = None,
    figures: str = None,
    lines: str = None,
    sections: str = None,
    headerfooter: str = None,
    pages: tuple = None,
) -> feedback.renderer.content.HTMLPageContents:
    """Load data to present as html view.

    images: there are more than one images folder possible
    """
    assert all((isinstance(item, str) or item is None)
               for item in [text, textposition, boxes, hits, horizontals])

    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text=text,
        textpositions=textposition,
        fontheader=fontheader,
        fontcontent=fontcontent,
        fill_empty=False,  # required if only some pages are selected
        pages=pages,
    )

    oneline = serializeraw.create_pagetextnavigators_fromfile(
        oneline_text,
        oneline_textposition,
        oneline_fontheader,
        oneline_fontcontent,
        fill_empty=False,
        mode=texmex.PageTextNavigatorMode.HORIZONTAL,
        pages=pages,
    )
    borders = serializeraw.load_pageborders(borders, pages=pages)

    alignment = load_alignment(alignment, pages=pages) if alignment else None  # pylint:disable=E1123
    alignment = fix_alignment(alignment, oneline)

    if isinstance(images, str):
        images = [images]
    if isinstance(figures, str):
        figures = [figures]

    boxes = serializeraw.load_boxes(boxes, pages=pages) if boxes else None
    if horizontals:
        horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    if lines:
        lines = serializeraw.load_lines(lines, pages=pages)
    hits = serializeraw.load_hits(hits, pages=pages) if hits else None
    if images:
        images = [
            feedback.renderer.images.zip_images(item, pages) for item in images
        ]
        images = utila.flatten(images)
    if figures:
        figures = [
            feedback.renderer.images.zip_images(item, pages) for item in figures
        ]
        figures = utila.flatten(figures)
        if images:
            # add loaded figures to images
            images.extend(figures)
        else:
            # no images are loaded
            images = figures

    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    ) if fontheader else None

    oneline_fontstore = serializeraw.create_fontstore(
        oneline_fontheader,
        oneline_fontcontent,
        pages=pages,
    ) if oneline_fontheader else None

    sections = serializeraw.load_sections(
        sections,
        pages=pages,
    ) if sections else None

    headerfooter = serializeraw.load_headerfooter(
        headerfooter,
        pages=pages,
    ) if headerfooter else None

    result = [
        load_page(
            alignment=alignment,
            border=borders,
            boxes=boxes,
            fontstore=fontstore,
            onelines=oneline,
            oneline_fontstore=oneline_fontstore,
            hits=hits,
            horizontals=horizontals,
            images=images,
            lines=lines,
            navigators=navigators,
            sections=sections,
            headerfooter=headerfooter,
            page=page.page,
        ) for page in borders
    ]
    return result


def load_page(
    border,
    page,
    navigators,
    fontstore,
    onelines,
    oneline_fontstore,
    sections,
    headerfooter,
    **kwargs,
):  # pylint:disable=R0914
    navigator = utila.select_page(navigators, page)
    oneline = utila.select_page(onelines, page)

    if headerfooter:
        headerfooter = utila.select_page(headerfooter, page)

    navigator_soc = soc(navigator, headerfooter)
    oneline_soc = soc(oneline, headerfooter)

    pagesize = utila.select_page(border, page).size
    alignment = kwargs.pop('alignment', None)
    if alignment:
        alignment = functools.partial(alignment.alignment, page=page)
    try:
        hits = utila.select_page(kwargs['hits'], page=page)
        border = hits.border if hits else []
    except ValueError:
        border = []

    boxes = select_page(kwargs, 'boxes', page)
    horizontals = select_page(kwargs, 'horizontals', page)
    lines = select_page(kwargs, 'lines', page)

    if select_layout(page, sections) == 'oneline':
        if oneline_fontstore:
            navigator = oneline
            fontstore = oneline_fontstore
            navigator_soc = oneline_soc

            def alignment(bounding):  # pylint:disable=W0613,function-redefined
                # justify all text
                return [textflow.alignment.style.TextAlignment.BLOCK]

        else:
            utila.error('could not select oneline layout, '
                        'there is no oneline fontstore available')

    images = feedback.renderer.images.select_images(kwargs.pop('images'), page)

    result = feedback.renderer.content.HTMLPageContent(
        alignment=alignment,
        border=border,
        boxes=boxes,
        fontstore=fontstore,
        navigator=navigator,
        oneline_fontstore=oneline_fontstore,
        oneline=oneline,
        pagesize=pagesize,
        horizontals=horizontals,
        images=images,
        lines=lines,
        navigator_soc=navigator_soc,
        page=page,
    )
    return result


def soc(navigator: texmex.PageTextNavigator, header) -> int:
    """Start of Content

    Empty page-textnavigator:
    >>> assert soc(None, None) is None
    """
    if not navigator:
        return None
    if not header:
        return None
    header = header.header
    if not header:
        return None
    end = header.end
    before = len(navigator.before(end))
    return before


def select_layout(page: int, sections: iamraw.Section) -> str:
    """\
    Note; This is a first weak approach.
    """
    if not sections:
        utila.log('require sections to perform layout selection - use default')
        return 'default'
    flat = utila.flatten(sections)
    for item in flat:
        if item.start != page or item.end != page:
            continue
        if isinstance(item, (
                iamraw.sections.TableOfContent,
                iamraw.sections.FigureTable,
                iamraw.sections.SymbolTable,
        )):
            return 'oneline'
    return 'default'


def select_page(args, key, page):
    try:
        result = utila.select_page(args[key], page=page)
        result = result.content if result else []
    except ValueError:
        result = []
    return result


def from_path(  # pylint:disable=R0914
    path: str,
    pages: tuple = None,
) -> feedback.renderer.content.HTMLPageContents:
    assert os.path.exists(path), str(path)
    text = iamraw.path.text(path)
    textposition = iamraw.path.textposition(path)
    oneline_text = iamraw.path.text(path, prefix='oneline')
    oneline_textposition = iamraw.path.textposition(path, prefix='oneline')
    borders = iamraw.path.sizeandborder(path)
    fontheader = iamraw.path.fontheader(path)
    fontcontent = iamraw.path.fontcontent(path)
    headerfooter = iamraw.path.headerfooters(path)
    oneline_fontheader = iamraw.path.fontheader(path, prefix='oneline')
    oneline_fontcontent = iamraw.path.fontcontent(path, prefix='oneline')
    alignment = textflow.path.alignment(path)
    boxes = iamraw.path.boxed(path)
    horizontals = iamraw.path.horizontals(path)
    lines = iamraw.path.line(path)
    sections_ = iamraw.path.sections_(path)  # pylint:disable=E1101
    hits = os.path.join(path, 'decider_border__detection_hits.yaml')
    # make border renderer optional
    fontheader = fontheader if os.path.exists(fontheader) else None
    fontcontent = fontcontent if os.path.exists(fontcontent) else None
    hits = hits if os.path.exists(hits) else None
    boxes = boxes if os.path.exists(boxes) else None
    horizontals = horizontals if os.path.exists(horizontals) else None
    lines = lines if os.path.exists(lines) else None
    headerfooter = headerfooter if os.path.exists(headerfooter) else None
    alignment = alignment if os.path.exists(alignment) else None
    sections_ = sections_ if os.path.exists(sections_) else None
    # TODO: INVESTIGATE HERE
    images = [os.path.join(path, 'rawmaker__images_images')]
    figures = [os.path.join(path, 'rawmaker__figures_figures')]
    loaded = load(
        borders=borders,
        alignment=alignment,
        boxes=boxes,
        text=text,
        textposition=textposition,
        fontcontent=fontcontent,
        fontheader=fontheader,
        hits=hits,
        horizontals=horizontals,
        images=images,
        figures=figures,
        lines=lines,
        oneline_text=oneline_text,
        oneline_textposition=oneline_textposition,
        oneline_fontheader=oneline_fontheader,
        oneline_fontcontent=oneline_fontcontent,
        sections=sections_,
        headerfooter=headerfooter,
        pages=pages,
    )
    return loaded


@textflow.serialize.loadme
def load_alignment(items):
    # TODO: MOVE TO WORDS

    def load_raw(item):
        item = item.replace('TextAlignment.', '')
        return textflow.alignment.style.TextAlignment[item]

    if isinstance(items, str):
        alignments = load_raw(items)
    else:
        alignments = [load_raw(item) for item in items]
    return alignments


def fix_alignment(alignment, oneline) -> textflow.alignment.info.AlignmentInfo:
    """Set none alignment pages to empty list.

    TODO: INVESTIGATE WHY ALIGNMENT CAN BE EMPTY.
    """
    if not alignment:
        return None
    # TODO: REMOVE AFTER FIXING DUMPING/LOADER
    alignment = [(item.page, utila.select_page(alignment, page=item.page))
                 for item in oneline]
    for page, content in alignment:
        if content is None:
            utila.error(f'no alignment for page: {page}')
    alignment = [
        item if item is not None else textflow.serialize.PageContent(
            page=page,
            content=[],
        ) for page, item in alignment
    ]

    result = textflow.alignment.info.AlignmentInfo(
        oneline,
        alignment,
    )
    return result
