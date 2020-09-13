# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import utila


def sections_(path: str, prefix: str = '') -> str:
    # TODO: REPLACE WITH IAMRAW CODE
    return utila.pathconnector(
        path,
        'sections',
        'section_result',
        prefix,
    )


iamraw.path.sections_ = sections_
