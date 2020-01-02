# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from tests import TEST_PATH

STATISTICA_TDATA = join(TEST_PATH, 'statistica/resources')
assert exists(STATISTICA_TDATA), STATISTICA_TDATA

STAT_SAMPLE_DATA = join(STATISTICA_TDATA, 'sample')
assert exists(STAT_SAMPLE_DATA), STAT_SAMPLE_DATA

SAMPLE_TEXT_STATISTICS = join(STAT_SAMPLE_DATA,
                              'analysis_statistica__statistics_chapters.yaml')
assert exists(SAMPLE_TEXT_STATISTICS), SAMPLE_TEXT_STATISTICS

SAMPLE_WORD_STATISTICS = join(STAT_SAMPLE_DATA,
                              'analysis_statistica__statistics_words.yaml')
assert exists(SAMPLE_WORD_STATISTICS), SAMPLE_WORD_STATISTICS

SAMPLE_GROUPME_TEXT = join(STAT_SAMPLE_DATA, 'groupme__chapter_chapter.yaml')
assert exists(SAMPLE_GROUPME_TEXT), SAMPLE_GROUPME_TEXT
