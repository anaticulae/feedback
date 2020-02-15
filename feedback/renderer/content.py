# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing

import iamraw

# TODO: MOVE TO IAMRAW
iamraw.TextContainers = typing.List[iamraw.TextContainer]


@dataclasses.dataclass
class HTMLPageContent:
    border: tuple = None
    content: iamraw.TextContainers = dataclasses.field(default_factory=list)
    dimension: iamraw.PageSize = None
    page: int = None


HTMLPageContents = typing.List[HTMLPageContent]
