# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utilo


def load_optimized(paths: list, pages: tuple = None) -> iamraw.PageFindings:
    for path in paths:
        if not utilo.exists(path):
            continue
        findings = serializeraw.load_grouped(path, pages=pages)
        return findings
    utilo.error(f'could not locate: {paths}')
    return []
