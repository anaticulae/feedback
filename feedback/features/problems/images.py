# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import feedback.renderer.images


def work(source: list, pages: tuple = None) -> list:  # pylint:disable=W0613
    result = []
    # TODO: SUPPORT SELECTIVE OUTPUT, REQUIRE START INDEX IN *.???
    # NOTE: WE EXTRACT FROM START TO END PAGES IS IGNORED
    result = []
    for item in source:
        images = feedback.renderer.images.load_images(item)
        if not images:
            continue
        for name, image in images:
            result.append((image, ext(name)))
    return result


def ext(name: str) -> str:
    return name.rsplit('.', maxsplit=1)[1]
