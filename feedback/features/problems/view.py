# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
import os

import protocol
import utila

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
        alignment: str,
        fontheader: str,
        fontcontent: str,
        images: str,
        boxes: str,
        horizontals: str,
        lines: str,
        hits: str,
        *linters: list,
        pages: tuple = None,
) -> list:
    """Generate html view for selected `pages`.

    TODO: define default parameter for source of protocol parameter

    Args:
        text(str): path to extract text
        textpositions(str): path to extracted text positions
        oneline_text(str): extracted text oneline layout
        oneline_textposition(str): extracted text positions oneline layout
        alignment: path to expected text alignment
        fontheader: path to extracted font header
        fontcontent: path to extracted font content
        images: path to load extracted images and information from
        hits(str): path to hits extracted from decider_border-hits
        boxes(str): path to extracted boxes
        horizontals(str): path to extracted horizontals
        lines(str): path to extracted lines
        linters(str): path to folder with linter results
        pages(tuple): selected pages to process
    Returns:
        List of extracted html view per page.
    """
    html = feedback.renderer.loader.load(
        text,
        textpositions,
        oneline_text,
        oneline_textposition,
        alignment=alignment,
        boxes=boxes,
        fontcontent=fontcontent,
        fontheader=fontheader,
        hits=hits,
        horizontals=horizontals,
        images=images,
        lines=lines,
        pages=pages,
    )
    findings = load_linters(linters)
    # collect marks from current working directory
    # TODO: IS THIS A DUPLICATION WITH *linters?
    root = str(os.getcwd())

    sentences = {}
    words = {}
    marks = load_marks(root, sentences, words)

    result = []
    for page in html:
        pagemarks = feedback.renderer.mark.create_configuration(
            marks=marks,
            page=page.page,
        )
        shapes = feedback.problems.shapy.determine_shapes(findings, page.page)
        rendered = feedback.renderer.html.render_page(
            page,
            pagemarks,
            shapes=shapes,
        )
        result.append(rendered)
    return result


def load_marks(path: str, sentences: dict, words: dict):
    collected = feedback.renderer.mark.collect(path)

    sentence_marks = convert_sentence_to_word_mark(collected, sentences, words)

    marks = {}
    if sentence_marks:
        marks.update(sentence_marks)
    if collected:
        # TODO: REMOVE SENTENCE MARKS
        marks.update(collected)
    return marks


def load_linters(paths: str):
    loaded = [protocol.load_result(path) for path in paths]
    loaded = utila.flatten(loaded)
    for index, item in enumerate(loaded):
        item.number = index
    return loaded


def convert_sentence_to_word_mark(marks: dict, sentences, words: dict) -> dict:
    assert isinstance(marks, dict), type(marks)
    assert isinstance(sentences, dict), type(sentences)
    # TODO: REPLACE WITH protocol.sentences()
    marks = {
        page: protocol.filter_mark(values, shortcut='s')
        for page, values in marks.items()
    }
    result = collections.defaultdict(list)
    for page, pagemarks in marks.items():
        for sentence_mark in pagemarks:
            # print(sentence_mark)
            # page = sentence_mark.page
            sentence_id = sentence_mark.location.value
            try:
                content = sentences[page][sentence_id]
            except (IndexError, KeyError):
                utila.error(f'could not locatate sentence: {sentence_id}'
                            f' on page {page}')
                continue
            try:
                pagewords = words[page]
            except KeyError:
                utila.error(f'could not sync sentence: {sentence_id}'
                            f' on page {page}')
                continue
            if selected is None:
                selected = feedback.renderer.mark.best_sync(pagewords, content)
                utila.error(f'could not sync sentence: {sentence_id}'
                            f' on page {page}')
                continue
            # TODO: REPLACE WITH PROTOCL
            selected = [
                protocol.Location.fromstr(f'w{item}p{page}')
                for item in selected
            ]
            result[page].append(selected)
    # enable KeyError
    result = dict(result)  # pylint:disable=R0204
    return result
