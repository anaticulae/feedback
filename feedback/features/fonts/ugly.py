# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import List
from typing import Tuple

from jinja2 import PackageLoader
from jinja2 import Template
from serializeraw import load_font_header
from utila import Flag
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load


# ('decider_fonts_iamugly', 'ugly'),
# ('rawmaker_fonts', 'hedaer'),
def work(iamugly_path: str, fontstore_path: str) -> Tuple[str, str, str]:
    fonts = load_font_header(fontstore_path)

    ugly = load(from_raw_or_path(iamugly_path), Loader=FullLoader)
    # border, hits = load_hits(hitspath)
    result_used = render_used_fonts(fonts)

    result_ugly = render_ugly_fonts(ugly)
    error = render_error([])
    return result_ugly, result_used, error


def render_error(ugly: list):
    errors = []
    # TODO: Create error module, EXPORT ERROR TYPES
    # page, index, box
    # for page, index, _ in hits:
    #     errors.append({
    #         'type': 'error',
    #         'module': PROCESS_NAME,
    #         'feature': FEATURE_NAME,
    #         'page': page,
    #         'object': index,
    #         'message':
    #         'Object ueberschreitet den Seitenrahmen',  # support id or direct message
    #     })

    # header = {
    #     'count': len(errors),
    #     'errors': errors,
    # }
    dumped = dump(errors)
    return dumped


def render_ugly_fonts(ugly):
    # - description: Do not use this peace of $h!t
    #   font: JCUGNO+NimbusSanL
    #   scale: 18.0    for item in ugly:
    loader = PackageLoader('feedback.features.fonts')
    ugly_template = Template(
        loader.get_source(None, 'fonts_ugly_badfont.html')[0])
    result = [
        (item['font'], item['scale'], item['description'], []) for item in ugly
    ]
    rendered = ugly_template.render(fonts=result)
    return rendered


def render_used_fonts(fonts: List) -> str:
    loader = PackageLoader('feedback.features.fonts')
    used_template = Template(loader.get_source(None, 'fonts_used.html')[0])

    sorted_fonts = sorted(
        fonts,
        key=lambda item: '%s %5.2f' % (item.name, item.scale),
    )
    rendered = used_template.render(fonts=sorted_fonts)
    return rendered


def name():
    return 'iamugly_view'


def commandline():
    return Flag(longcut=name(), message='export the html result of %s' % name())
