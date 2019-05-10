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

from tests import TEST_PATH

TEST_PATH_BORDER = join(TEST_PATH, 'border/data')

HITS = join(TEST_PATH_BORDER, 'hits')
assert exists(HITS), HITS
HITS_YAML = join(HITS, 'hitthebox__hits.yaml')
assert exists(HITS_YAML), HITS_YAML
