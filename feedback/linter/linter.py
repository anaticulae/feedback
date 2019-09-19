# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import typing

import protocol


def group_finding_bypage(items: typing.List[protocol.Finding]):
    result = collections.defaultdict(list)
    for item in items:
        result[item.location.page].append(item)

    # convert to normal dict to have KeyError's
    result = dict(result)
    return result
