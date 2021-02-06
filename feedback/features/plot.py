# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import painter
import serializeraw
import utila

import feedback.features.view


def work(
        sizeandborder: str,
        *linters: list,
        pages: tuple = None,
) -> typing.Tuple[bytes, bytes]:
    sizeandborder = serializeraw.load_pageborders(sizeandborder, pages)
    maxpage = max([page.page for page in sizeandborder])

    with utila.profile('load findings'):
        findings: iamraw.PageFindings = feedback.features.view.load_findings(
            linters,
            pages=pages,
        )

    findings_histogram = render_findings_overview(findings, maxpage)
    findings_pie = render_findings_types(findings)

    return findings_histogram, findings_pie


def render_findings_overview(
        findings: iamraw.PageFindings,
        maxpage: int,
) -> bytes:
    pages = utila.ranged_list(maxpage)
    counted = [
        len(utila.select_page(
            findings,
            page=page,
            default=[],
        )) for page in pages
    ]
    if not pages:
        utila.debug('no findings given, skip plotting findings')
        return utila.NO_RESULT
    rendered = painter.bar_render(
        x=pages,
        y=counted,
        xlim=(0, maxpage),
        width=20.0,
        height=0.75 * golden(15.0),
        grid=True,
        xlabel='Seite',
        ylabel='Anzahl',
    )
    raw = painter.png(rendered)
    return raw


def render_findings_types(findings: iamraw.PageFindings) -> bytes:
    return utila.NO_RESULT


def golden(longest: float) -> float:
    # TODO: REPLACE WITH UTILA
    return longest / 1.618
