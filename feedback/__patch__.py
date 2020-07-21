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


def create_pagetextnavigators(  # pylint:disable=R0914
        text: iamraw.Document,
        text_positions,
        fontstore: iamraw.FontStore = None,
        fill_empty: bool = True,
        mode=texmex.PageTextNavigatorMode.BOTH,
) -> texmex.PageTextNavigators:
    result = []
    for textpage in text:
        page = textpage.page
        navigator = texmex.PageTextNavigator(
            size=text.dimension,
            page=page,
        )
        textid = 0
        textposition = utila.select_page(text_positions, page)
        # remove horizontal or vertical text container
        content = select_textcontainer(textpage, mode=mode)

        for item in content:
            try:
                lines = item.lines
            except AttributeError:
                continue
            pos, mean = textposition.content[textid]
            for index, line in enumerate(lines):
                bounding = iamraw.split_y(pos, index, len(lines))
                if fontstore:
                    for char_number, char in enumerate(line.chars):
                        fontid = fontstore.fontid(
                            page,
                            textid,
                            index,
                            char_number,
                        )
                        char.font = fontid
                style = texmex.style.create_textstyle(line.chars)
                # TODO: Remove strip after container is fixed
                if not line.text.strip():
                    # skip bad removed rawmaker extraction
                    continue
                navigator.insert(
                    text=line.text,
                    style=style,
                    bounding=bounding,
                    bounding_mean=mean,
                )
            textid += 1
        result.append(navigator)

    if fill_empty:
        result = fill_empty_navigators(result, dimension=text.dimension)
    return result


texmex.create_pagetextnavigators = create_pagetextnavigators


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


def select_textcontainer(content, mode: texmex.PageTextNavigatorMode):
    if not content:
        return content

    if mode == texmex.PageTextNavigatorMode.HORIZONTAL:
        content = [
            item for item in content if isinstance(item, iamraw.TextContainer)
        ]
        return content

    if mode == texmex.PageTextNavigatorMode.VERTICAL:
        content = [
            item for item in content
            if isinstance(item, iamraw.VerticalTextContainer)
        ]
        return content
    return content


def sections_(path: str, prefix: str = '') -> str:
    # TODO: REPLACE WITH IAMRAW CODE
    return utila.pathconnector(
        path,
        'sections',
        'section_result',
        prefix,
    )


iamraw.path.sections_ = sections_
