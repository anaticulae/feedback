# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import feedback.renderer.images


def work(source: list, pages: tuple = None) -> typing.List[bytes]:  # pylint:disable=W0613
    result = []
    for item in source:
        images = feedback.renderer.images.load_images(item)
        if not images:
            continue
        for image in images:
            result.append((image.raw, image.ext))
    return result
