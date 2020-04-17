# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import iamraw
import iamraw.path
import serializeraw
import texmex
import textflow.features.alignment
import textflow.path
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
        alignment: str = None,
        boxes: str = None,
        fontcontent: str = None,
        fontheader: str = None,
        hits: str = None,
        horizontals: str = None,
        images: list = None,
        lines: str = None,
        pages: tuple = None,
) -> feedback.renderer.content.HTMLPageContents:
    """Load data to present as html view.

    images: there are more than one images folder possible
    """
    assert all((isinstance(item, str) or item is None)
               for item in [text, textposition, boxes, hits, horizontals])

    text = serializeraw.load_document(text, pages=pages)
    textposition = serializeraw.load_textpositions(textposition, pages=pages)
    oneline_navigators = serializeraw.create_pagetextnavigators_fromfile(
        oneline_text,
        oneline_textposition,
        mode=texmex.PageTextNavigatorMode.HORIZONTAL,
        pages=pages,
    )

    alignment = load_alignment(alignment, pages=pages) if alignment else None  # pylint:disable=E1123
    if alignment:
        alignment = textflow.alignment.info.AlignmentInfo(
            oneline_navigators,
            alignment,
        )
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
    fontstore = None
    if fontheader:
        fontstore = serializeraw.create_fontstore(
            fontheader,
            fontcontent,
            pages=pages,
        )
    result = [
        load_page(
            text.dimension,
            fontstore,
            alignment=alignment,
            boxes=boxes,
            hits=hits,
            horizontals=horizontals,
            images=images,
            lines=lines,
            text=page,
            textposition=textposition,
        ) for page in text
    ]
    return result


def load_page(dimension, fontstore: iamraw.FontStore, **kwargs):  # pylint:disable=R0914
    text = kwargs.pop('text')
    # TODO: DETECT DIMENSION OUT OF TEXT
    page = text.page
    textposition = utila.select_page(kwargs.pop('textposition'), page=page)
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

    images = feedback.renderer.images.select_images(kwargs.pop('images'), page)

    # skip non TextContainer boxes - for example LTRect
    selected = [
        item for item in text.children if isinstance(item, iamraw.TextContainer)
    ]
    fill_fonts(selected, page, fontstore)
    for index, children in enumerate(text):
        # update with loaded text position
        children.box = textposition.content[index][0]
    result = feedback.renderer.content.HTMLPageContent(
        alignment=alignment,
        border=border,
        boxes=boxes,
        content=selected,
        dimension=dimension,
        horizontals=horizontals,
        images=images,
        lines=lines,
        page=page,
    )
    return result


def select_page(args, key, page):
    try:
        result = utila.select_page(args[key], page=page)
        result = result.content if result else []
    except ValueError:
        result = []
    return result


def from_path(
        path: str,
        pages: tuple = None,
) -> feedback.renderer.content.HTMLPageContents:
    assert os.path.exists(path), str(path)
    text = iamraw.path.text(path)
    textposition = iamraw.path.textposition(path)
    oneline_text = iamraw.path.text(path, prefix='oneline')
    oneline_textposition = iamraw.path.textposition(path, prefix='oneline')
    fontheader = iamraw.path.fontheader(path)
    fontcontent = iamraw.path.fontcontent(path)
    alignment = textflow.path.alignment(path)
    boxes = iamraw.path.boxed(path)
    horizontals = iamraw.path.horizontals(path)
    lines = iamraw.path.line(path)
    hits = os.path.join(path, 'decider_border__detection_hits.yaml')
    # make border renderer optional
    fontheader = fontheader if os.path.exists(fontheader) else None
    fontcontent = fontcontent if os.path.exists(fontcontent) else None
    hits = hits if os.path.exists(hits) else None
    boxes = boxes if os.path.exists(boxes) else None
    horizontals = horizontals if os.path.exists(horizontals) else None
    lines = lines if os.path.exists(lines) else None
    alignment = alignment if os.path.exists(alignment) else None
    # TODO: INVESTIGATE HERE
    images = [os.path.join(path, 'rawmaker__images_images')]
    loaded = load(
        alignment=alignment,
        boxes=boxes,
        fontcontent=fontcontent,
        fontheader=fontheader,
        hits=hits,
        horizontals=horizontals,
        images=images,
        lines=lines,
        oneline_text=oneline_text,
        oneline_textposition=oneline_textposition,
        text=text,
        textposition=textposition,
        pages=pages,
    )
    return loaded


def fill_fonts(text, page, fontstore: iamraw.FontStore):
    # TODO: MOVE THIS HACK/ IS THIS A HACK?
    if not fontstore:
        return
    for container_id, container in enumerate(text):
        for line_id, line in enumerate(container):
            for char_id, char in enumerate(line):
                fontid = fontstore.fontid(page, container_id, line_id, char_id)
                font = fontstore[fontid]
                flags = list(font.flags)
                if font.style == iamraw.Style.ITALIC:
                    flags.append(iamraw.FontFlag.Italic)
                char.flags = tuple(flags)
                char.font = font.name


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
