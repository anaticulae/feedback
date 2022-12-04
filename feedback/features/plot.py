# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import painter
import protocol
import serializeraw
import utila

import feedback.features

LABEL_COUNT_MAX = configo.HV_INT_PLUS(default=50)


def work(
    pagenumbers: str,
    optimized: str,
    pages: tuple = None,
) -> tuple[bytes, bytes]:
    with utila.profile('load findings'):
        findings = feedback.features.load_optimized(optimized, pages=pages)
    pagenumbers = serializeraw.load_pagenumbers_magic(
        pagenumbers,
        pages=pages,
    )
    findings_histogram = render_findings_overview(
        findings,
        pagenumbers=pagenumbers,
    )
    findings_pie = render_findings_types(findings)
    return findings_histogram, findings_pie


def render_findings_overview(
    findings: iamraw.PageFindings,
    pagenumbers: dict,
) -> bytes:
    # use one base for better user experience
    # plus one for matlab rendering
    pages = pages_select(
        pagenumbers.values(),
        pages_count_max=LABEL_COUNT_MAX,
    )
    if not pages:
        utila.debug('no findings given, skip plotting findings')
        return utila.NO_RESULT
    counted = [
        len(utila.select_page(
            findings,
            page=page,
            default=[],
        )) for page in pagenumbers.keys()
    ]
    ylim = max(max(counted) + 1, 5)
    rendered = painter.bar_render(
        x=pages,
        y=counted,
        ylim=(0, ylim),
        width=20.0,
        height=0.75 * golden(15.0),
        grid=True,
        xlabel='Seite',
        ylabel='Anzahl',
        intlabel=(False, True),
    )
    raw = painter.png(rendered)
    return raw


def pages_select(pagenumbers, pages_count_max: int = 50) -> list:
    """\
    >>> pages_select([1, 2, 3, 4, 5, 6, 7, 8], pages_count_max=50)
    ['1', '2', '3', '4', '5', '6', '7', '8']
    >>> pages_select(utila.rlist(0, 133), pages_count_max=50)
    ['0', '1', '3',...'127', '129', '131', '132']
    """
    assert pages_count_max > 0, pages_count_max
    # TODO: GENERALIZE AND MOVE TO UTILA
    if not pagenumbers:
        return []
    pagenumbers = [str(item) for item in pagenumbers]
    if len(pagenumbers) < pages_count_max:
        return pagenumbers
    step = int(len(pagenumbers) / pages_count_max)
    result = [str(pagenumbers[0])]
    for pagenumber in pagenumbers[1:len(pagenumbers):step]:
        result.append(str(pagenumber))
    last = str(pagenumbers[-1])
    if result[-1] != last:
        result.append(last)
    return result


def render_findings_types(findings: iamraw.PageFindings) -> bytes:
    # TODO: REFACTOR IMPORT AFTER UPGRADING
    findings = protocol.flat(findings)
    typed = bytype(findings)

    labels = ['Fehler', 'Warnung', 'Vorschlag']
    counted = [len(typed[item]) for item in 'EWI']

    labels = [item for item, count in zip(labels, counted) if count]
    counted = [item for item in counted if item]

    rendered = painter.pie_render(
        x=counted,
        labels=labels,
        absolute=True,
        width=7.15,
        height=4.15,
    )
    raw = painter.png(rendered)
    return raw


def bytype(items: iamraw.Findings) -> dict:
    """Group findings by `finding.msgid`."""
    # TODO: REPLACE WITH PROTOCOL CODE
    result = {'E': [], 'W': [], 'I': []}
    for item in items:
        msgid = str(item.solution.msgid)[0].upper()
        try:
            result[msgid].append(item)
        except KeyError:
            result['I'].append(item)
    return result


def golden(longest: float) -> float:
    # TODO: REPLACE WITH UTILA
    return longest / 1.618
