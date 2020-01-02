# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import jinja2


def template(package: str, file: str):
    templates = os.path.split(__file__)[0]
    loader = jinja2.FileSystemLoader(templates)
    file = f'{package}/{file}'
    result = jinja2.Template(loader.get_source(None, file)[0])
    return result
