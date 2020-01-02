# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import feedback.renderer.html


def work(text: str, textpositions: str, pages: tuple = None) -> list:
    result = []

    html = feedback.renderer.html.load(text, textpositions, pages=pages)

    result = [feedback.renderer.html.render_page(item) for item in html]

    return result
