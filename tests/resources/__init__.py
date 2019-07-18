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

RESTRUCTED_HEADLINES = join(RESTRUCTED, 'words__headlines_headlines.yaml')
RESTRUCTED_TEXT = join(RESTRUCTED, 'words__text_text.yaml')
RESTRUCTED_LISTS = join(RESTRUCTED, 'words__list_list.yaml')
RESTRUCTED_BOXEDCONTENT = join(RESTRUCTED, 'words__boxed_boxed.yaml')
RESTRUCTED_RESULT = join(RESTRUCTED, 'words__words_result.yaml')
RESTRUCTED_SECTIONS = join(RESTRUCTED, 'sections__sections_result.yaml')
RESTRUCTED_PAGENUMBERS = join(RESTRUCTED,
                              'groupme__pagenumbers_pagenumbers.yaml')

RESOURCES = [
    RESTRUCTED,
    RESTRUCTED_BOXEDCONTENT,
    RESTRUCTED_HEADLINES,
    RESTRUCTED_LISTS,
    RESTRUCTED_PAGENUMBERS,
    RESTRUCTED_RESULT,
    RESTRUCTED_SECTIONS,
    RESTRUCTED_TEXT,
    TEST_RESOURCES,
]

for item in RESOURCES:
    assert exists(item), str(item)
