# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from feedback import ROOT

TEST_RESOURCES = join(ROOT, 'tests/resources')

RESTRUCTED = join(TEST_RESOURCES, 'restruct')

RESOURCES = [
    TEST_RESOURCES,
    RESTRUCTED,
]

for item in RESOURCES:
    assert exists(item), str(item)
