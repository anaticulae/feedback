# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import Tuple

from serializeraw import load_hits
from utila import Flag
from yaml import dump

import feedback.templates


def work(hitspath: str) -> Tuple[str, str]:
    border, hits = load_hits(hitspath)
    result = render(border, hits)
    error = render_error(hits)
    return result, error


def render_error(hits: list):
    from feedback.command.decider.border import FEATURE_NAME
    from feedback.command.decider.border import PROCESS_NAME
    errors = []
    # TODO: Create error module, EXPORT ERROR TYPES
    # page, index, box
    for page, index, _ in hits:
        errors.append({
            'type': 'error',
            'module': PROCESS_NAME,
            'feature': FEATURE_NAME,
            'page': page,
            'object': index,
            'message':
            'Object ueberschreitet den Seitenrahmen',  # support id or direct message
        })

    header = {
        'count': len(errors),
        'errors': errors,
    }
    dumped = dump(header)
    return dumped


def render(border, hits: list) -> str:
    template = feedback.templates.template('border', 'hits.html')
    rendered = template.render(border=border, hits=hits)
    return rendered


def name():
    return 'hitthebox'


def commandline():
    return Flag(longcut=name(), message='export the html result of %s' % name())
