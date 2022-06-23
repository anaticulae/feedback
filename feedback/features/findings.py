# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import ghost
import iamraw
import serializeraw
import utila

import feedback.features


def work(
    sentence_bounding: str,
    document: str,
    inputs: tuple,
    outputs: str,
    pages: tuple = None,
):
    utila.debug(f'pdf: {document}')
    findings, sentence_bounding = load_resources(
        inputs,
        sentence_bounding,
        pages=pages,
    )
    prepared = prepare_findings(findings)
    if not prepared:
        utila.error('could not render any findings')
        return utila.NO_RESULT
    if not utila.exists(document):
        utila.error(f'--pdf {document} does not exists')
        return utila.NO_RESULT
    ghost.run(
        src=document,
        dst=outputs,
        boundings=prepared,
    )
    return utila.NO_RESULT


def load_resources(inputs, sentence_bounding, pages: tuple = None):
    utila.debug(f'dir: {inputs}')
    with utila.profile('load findings'):
        findings = feedback.features.load_optimized(inputs, pages=pages)
    if utila.exists(sentence_bounding):
        sentence_bounding = serializeraw.load_sentence_bounding(
            source=sentence_bounding,
            pages=pages,
        )
    else:
        sentence_bounding = []
    return findings, sentence_bounding


OVERLAY_COLOR = (255, 0, 0, 50)


def prepare_findings(findings: list) -> list:
    findings: list = utila.flatten_content(findings)
    findings = [
        item for item in findings
        if isinstance(item.location, iamraw.BoundingLocation)
    ]
    result = []
    for item in findings:
        fname = item.number
        page = item.location.page
        bounding = ghost.bounding_convert(item.location.value)
        result.append(
            ghost.Part(
                page=page,
                bounding=bounding,
                name=fname,
                color=OVERLAY_COLOR,
            ))
    return result
