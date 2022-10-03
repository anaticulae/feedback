# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import copy

import ghost
import iamraw
import serializeraw
import utila

import feedback.features


def work(
    sentence_bounding: str,
    optimized: str,
    document: str,
    outputs: str,
    pages: tuple = None,
):
    utila.debug(f'pdf: {document}')
    findings, sentence_bounding = load_resources(
        optimized,
        sentence_bounding,
        pages=pages,
    )
    prepared = prepare_findings(findings, sentence_bounding)
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
        if sentence_bounding:
            maxpage = sentence_bounding[-1].page
            sentence_bounding = [
                utila.select_content(sentence_bounding, page=page, default=[])
                for page in utila.rlist(maxpage + 1)
            ]
    else:
        sentence_bounding = []
    return findings, sentence_bounding


OVERLAY_COLOR = (255, 0, 0, 50)


def prepare_findings(findings: list, sentence_bounding: list) -> list:
    findings: list = utila.flatten_content(findings)
    selected = []
    for finding in findings:
        if isinstance(finding.location, iamraw.BoundingLocation):
            selected.append(finding)
            continue
        if finding.location.shortcut == 's':
            try:
                loca = finding.location
                sentence = sentence_bounding[loca.page][loca.value]
            except IndexError:
                utila.error(f'missing sentence bounding: {loca}')
                continue
            # TODO: MAY CHANGE THIS LATER
            finding = copy.deepcopy(finding)
            finding.location = iamraw.BoundingLocation(
                page=loca.page,
                value=sentence,
            )
            selected.append(finding)
            continue
    result = []
    for finding in selected:
        fname = finding.number
        page = finding.location.page
        if not (bounding := bounding_convert(finding.location.value)):  # pylint:disable=superfluous-parens
            utila.error(f'invalid location: {finding}\n')
            continue
        result.append(
            ghost.Part(
                page=page,
                bounding=bounding,
                name=fname,
                color=OVERLAY_COLOR,
            ))
    return result


def bounding_convert(bounding) -> list:
    if not bounding:
        return None
    single = isinstance(bounding[0], (int, float))
    if single:
        bounding = [bounding]
    bounding = [ghost.bounding_convert(bbox) for bbox in bounding]
    return bounding
