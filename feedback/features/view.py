# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The view module generates the html representation of the pdf data
structure. Furthermore the linter results are added to view the problems
in user document.

In the current state text and horizontal lines are printed.
"""

import collections
import copy
import os

import iamraw
import protoerror
import serializeraw
import utilo

import feedback.features
import feedback.problems.shapy
import feedback.renderer.html
import feedback.renderer.loader
import feedback.renderer.mark
import feedback.renderer.shape


def work(  # pylint:disable=R0914,too-many-arguments
    text: str,
    textpositions: str,
    oneline_text: str,
    oneline_textposition: str,
    sizeandborders: str,
    alignment: str,
    fontheader: str,
    fontcontent: str,
    ximages: list,
    xfigures: list,
    boxes: str,
    horizontals: str,
    lines: str,
    hits: str,
    words: str,
    sections: str,
    headerfooter: str,
    optimized: list,
    pages: tuple = None,
) -> list:
    """Generate html view for selected `pages`.

    TODO: define default parameter for source of protoerror parameter

    Args:
        text(str): path to extract text
        textpositions(str): path to extracted text positions
        oneline_text(str): extracted text oneline layout
        oneline_textposition(str): extracted text positions oneline layout
        sizeandborders: path to page size information
        alignment: path to expected text alignment
        fontheader: path to extracted font header
        fontcontent: path to extracted font content
        ximages: path to load extracted images and information from
        xfigures: path to extracted figures and figure informations
        hits(str): path to hits extracted from decider_border-hits
        boxes(str): path to extracted boxes
        horizontals(str): path to extracted horizontals
        lines(str): path to extracted lines
        words(path): path to extracted sentences
        sections(path): path to extracted sections
        headerfooter(path): path to extracted headerfooter
        optimized(str): path to folder with linter results
        pages(tuple): selected pages to process
    Returns:
        List of extracted html view per page.
    """
    sections = sections if os.path.exists(sections) else None
    with utilo.profile('load resources'):
        html = feedback.renderer.loader.load(
            text,
            textpositions,
            oneline_text,
            oneline_textposition,
            borders=sizeandborders,
            alignment=alignment,
            boxes=boxes,
            fontcontent=fontcontent,
            fontheader=fontheader,
            hits=hits,
            horizontals=horizontals,
            images=ximages,
            figures=xfigures,
            lines=lines,
            sections=sections,
            headerfooter=headerfooter,
            pages=pages,
        )
    with utilo.profile('load findings'):
        findings = feedback.features.load_optimized(optimized, pages=pages)
    with utilo.profile('prepare data'):
        pagesentences = load_sentences(words, pages=pages)
        pagewords = load_single_words(html)
        marks = load_marks(findings, pagesentences, pagewords)
    result = []
    with utilo.profile('render result'):
        for page in html:
            pagemarks = feedback.renderer.mark.create_configuration(
                marks=marks,
                page=page.page,
            )
            shapes = feedback.problems.shapy.determine_shapes(
                findings,
                page.page,
            )
            rendered = feedback.renderer.html.render_page(
                page,
                pagemarks,
                shapes=shapes,
            )
            result.append(rendered)
    return result


def load_sentences(path: str, pages: tuple = None) -> dict:
    words = serializeraw.load_text(path, pages=pages)
    pagesentences = collections.defaultdict(list)
    for item in words:
        for _, sentences in item.content:
            for sentence in sentences:
                pagesentences[item.page].append(sentence)
    # enable KeyError
    pagesentences = dict(pagesentences)  # pylint:disable=R0204
    return pagesentences


def load_single_words(navigators):
    result = {}
    for htmlpage in navigators:
        generator = feedback.renderer.mark.WordGenerator()
        collected = []
        if htmlpage.navigator:
            for line in htmlpage.navigator:
                for _, word in generator.words(line.text):
                    collected.append(word)
        result[htmlpage.page] = collected
    return result


def load_marks(
    findings: iamraw.PageFindings,
    sentences: dict,
    words: dict,
) -> dict:
    marks = collections.defaultdict(list)
    if findings:
        # TODO: REMOVE SENTENCE MARKS
        for grouped in findings:
            marks[grouped.page].extend(grouped.content)

    sentence_marks = convert_sentence_to_word_mark(findings, sentences, words)
    if sentence_marks:
        for page, values in sentence_marks.items():
            marks[page].extend(values)
    # enable KeyError
    marks = dict(marks)  # pylint:disable=R0204
    return marks


def load_marks_from_path(source, page: int):
    html = feedback.renderer.loader.from_path(source)
    findings = protoerror.findings_from_path(source)
    pagesentences = load_sentences(iamraw.path.words_text(source))
    pagewords = load_single_words(html)
    marks = load_marks(findings, pagesentences, pagewords)

    pagemarks = feedback.renderer.mark.create_configuration(
        marks=marks,
        page=page,
    )
    return pagemarks


def convert_sentence_to_word_mark(
    marks: iamraw.PageFindings,
    sentences,
    words: dict,
) -> dict:
    assert isinstance(sentences, dict), type(sentences)
    marks = {
        grouped.page: protoerror.sentences(grouped.content) for grouped in marks
    }
    result = collections.defaultdict(list)
    for page, pagemarks in marks.items():
        for sentence_mark in pagemarks:
            sentence_id = sentence_mark.location.value
            try:
                content = sentences[page][sentence_id]
            except (IndexError, KeyError):
                utilo.error(f'could not locatate sentence: {sentence_id}'
                            f' on page {page}')
                continue
            try:
                pagewords = words[page]
            except KeyError:
                utilo.error(f'could not sync sentence: {sentence_id}'
                            f' on page {page}')
                continue
            selected = feedback.renderer.mark.best_sync(pagewords, content)
            if selected is None:
                utilo.error(f'could not sync sentence: {sentence_id}'
                            f' on page {page}')
                continue
            # TODO: REPLACE WITH PROTOCL
            word_findings = []
            for item in selected:
                # TODO: IS COPY NECESSARY?
                new = copy.deepcopy(sentence_mark)
                new.location = iamraw.Location.from_word(word=item, page=page)
                word_findings.append(new)
            result[page].extend(word_findings)
    # enable KeyError
    result = dict(result)  # pylint:disable=R0204
    return result
