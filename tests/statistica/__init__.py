# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from tests import TEST_PATH

STATISTICA_TEST_DATA = join(TEST_PATH, 'statistica/data')
assert exists(STATISTICA_TEST_DATA), STATISTICA_TEST_DATA

SAMPLE_MEASURE = join(STATISTICA_TEST_DATA, 'sample/measure.yaml')
assert exists(SAMPLE_MEASURE), SAMPLE_MEASURE

SAMPLE_OCCURENCE = join(STATISTICA_TEST_DATA, 'sample/occurence.yaml')
assert exists(SAMPLE_OCCURENCE), SAMPLE_OCCURENCE

SAMPLE_ALPHA = join(STATISTICA_TEST_DATA, 'sample/toc_and_chapter.yaml')
assert exists(SAMPLE_ALPHA), SAMPLE_ALPHA
