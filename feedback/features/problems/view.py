# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import feedback.renderer.html
import feedback.renderer.mark


def work(text: str, textpositions: str, pages: tuple = None) -> list:
    """Generate html view for selected `pages`.

    TODO: define default parameter for source of protocol parameter

    Args:
        text(str): path to extract text
        textpositions(str): path to extracted text positions
        pages(tuple): selected pages to process
    Returns:
        List of extracted html view per page.
    """
    html = feedback.renderer.html.load(text, textpositions, pages=pages)

    # collect marks from current working directory
    root = str(os.getcwd())
    marks = feedback.renderer.mark.collect(root)

    result = []
    for page in html:
        pagemarks = feedback.renderer.mark.create_configuration(
            marks=marks,
            page=page.page,
        )
        rendered = feedback.renderer.html.render_page(page, pagemarks)
        result.append(rendered)
    return result
