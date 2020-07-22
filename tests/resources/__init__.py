# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import feedback

power.setup(feedback.ROOT)

RESTRUCTED_PDF = power.DOCU27_PDF
PORTING_PYTHON3_PDF = power.DOCU09_PDF
MASTER72_PDF = power.MASTER072_PDF

LEFTRIGHT = power.BOOK007_PDF
LEFTRIGHT_GENERATED = power.link(power.BOOK007_PDF)

BACHELOR56 = power.link(power.BACHELOR056_PDF)
BACHELOR56_PDF = power.BACHELOR056_PDF

BACHELOR90 = power.link(power.BACHELOR090_PDF)
BACHELOR90_PDF = power.BACHELOR090_PDF

MASTER116 = power.link(power.MASTER116_PDF)
MASTER116_PDF = power.MASTER116_PDF

MASTER72_GENERATED = power.link(power.MASTER072_PDF)

GENERATED_PORTING_PYTHON3 = power.link(power.DOCU09_PDF)

# test after running generation step in update.py
REQUIRED_RESOURCES = [
    BACHELOR56,
    BACHELOR56_PDF,
    BACHELOR90,
    BACHELOR90_PDF,
    GENERATED_PORTING_PYTHON3,
    LEFTRIGHT,
    LEFTRIGHT_GENERATED,
    MASTER116,
    MASTER116_PDF,
    MASTER72_GENERATED,
    MASTER72_PDF,
]
