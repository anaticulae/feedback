# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import iamraw
import texmex
import textflow.alignment.info
import utilo

import feedback.renderer.images as fri


@dataclasses.dataclass
class HTMLPageContent:
    alignment: textflow.alignment.info.AlignmentInfo = None
    border: tuple = None
    boxes: utilo.Rectangles = dataclasses.field(default_factory=list)
    navigator: texmex.PTN = None
    fontstore: iamraw.FontStore = None
    oneline: texmex.PTN = None
    oneline_fontstore: iamraw.FontStore = None
    pagesize: iamraw.PageSize = None
    images: fri.ZippedImageInfos = dataclasses.field(default_factory=list)
    horizontals: utilo.Rectangles = dataclasses.field(default_factory=list)
    lines: utilo.Rectangles = dataclasses.field(default_factory=list)
    navigator_soc: int = None
    page: int = None

    def __repr__(self):
        result = f'HTMLPageContent(page={self.page}, border={self.border}, pagesize={self.pagesize})'
        return result


HTMLPageContents = list[HTMLPageContent]
