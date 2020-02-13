# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import protocol


def group_finding_bypage(items: typing.List[protocol.Finding]) -> dict:
    # TODO: MOVE TO PROTOCOL
    collected = collections.defaultdict(list)
    for item in items:
        collected[item.location.page].append(item)

    # convert to normal dict to have KeyError's
    result = dict(collected)
    return result
