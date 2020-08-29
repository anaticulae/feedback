# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import iamraw.path
import texmex
import utila

# TODO: MOVE TO TEXMEX


def fill_empty_navigators(
        navigators: texmex.PageTextNavigators,
        dimension: iamraw.PageSize,
) -> texmex.PageTextNavigators:
    """Some documents contain white pages. White pages contain no
    text and therefore no text_positions. The document [CONTENT,
    WHITEPAGE, CONTENT, CONTENT] produces the pagetextnavigators
    page =[0,2,3]. If we assume that some algorithm requires a
    closed row of navigators this can lead to problems.Therefore we
    insert an empty PageTextNavigator at position 1 to avoid these
    problems.
    """
    if not navigators:
        return []
    # require ascending list for while loop below
    navigators = sorted(navigators, key=lambda x: x.page)
    filled = [navigators[0]]
    for item in navigators[1:]:
        # fill empty
        while filled[-1].page + 1 < item.page:
            navigator = texmex.PageTextNavigator(
                size=dimension,
                page=filled[-1].page + 1,
            )
            filled.append(navigator)
        filled.append(item)
    return filled


def sections_(path: str, prefix: str = '') -> str:
    # TODO: REPLACE WITH IAMRAW CODE
    return utila.pathconnector(
        path,
        'sections',
        'section_result',
        prefix,
    )


iamraw.path.sections_ = sections_
