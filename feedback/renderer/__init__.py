# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import os
import typing

import iamraw


@dataclasses.dataclass
class HTMLPageContent:
    dimension: iamraw.PageSize = None
    page: int = None
    content: typing.List[iamraw.TextContainer] = \
                                         dataclasses.field(default_factory=list)


HTMLPageContents = typing.List[HTMLPageContent]
