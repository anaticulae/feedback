# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os
from os.path import exists
from os.path import join

from feedback import ROOT

RESOURCES = join(ROOT, 'tests/resources')

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
MASTER = os.path.join(RESOURCES, 'master')

GENERATED = os.path.join(RESOURCES, 'generated')

RESTRUCTED = join(GENERATED, 'docu_restructuredtext')
RESTRUCTED_HEADLINES = join(RESTRUCTED, 'words__headlines_headlines.yaml')
RESTRUCTED_TEXT = join(RESTRUCTED, 'words__text_text.yaml')
RESTRUCTED_LISTS = join(RESTRUCTED, 'words__list_list.yaml')
RESTRUCTED_BOXEDCONTENT = join(RESTRUCTED, 'words__boxed_boxed.yaml')
RESTRUCTED_RESULT = join(RESTRUCTED, 'words__word_result.yaml')
RESTRUCTED_SECTIONS = join(RESTRUCTED, 'sections__section_result.yaml')
RESTRUCTED_PAGENUMBERS = join(RESTRUCTED, 'groupme__pagenumbers_pagenumbers.yaml') # yapf:disable
RESTRUCTED_USERLINTING = join(RESTRUCTED, 'decider__titlepage_user.yaml')

RESTRUCTED_PDF = join(DOCU, 'restructuredtext.pdf')
PORTING_PYTHON3_PDF = join(DOCU, 'porting_extension_modules.pdf')
MASTER72_PDF = join(MASTER, 'page_72_noimages_toc.pdf')

LEFTRIGHT = join(BOOK, 'leftright.pdf')
LEFTRIGHT_GENERATED = os.path.join(GENERATED, 'book_leftright')

BACHELOR56 = os.path.join(GENERATED, 'bachelor_page_56_hard_to_read')
BACHELOR56_PDF = os.path.join(BACHELOR, 'page_56_hard_to_read.pdf')

MASTER72_GENERATED = os.path.join(GENERATED, 'master_page_72_noimages_toc')
GENERATED_PORTING_PYTHON3 = os.path.join(GENERATED, 'docu_porting_extension_modules') # yapf:disable
GENERATED_RESTRUCTED = RESTRUCTED

# test after running generation step in update.py
REQUIRED_RESOURCES = [
    BACHELOR,
    BACHELOR56,
    BACHELOR56_PDF,
    GENERATED,
    GENERATED_PORTING_PYTHON3,
    GENERATED_RESTRUCTED,
    LEFTRIGHT,
    LEFTRIGHT_GENERATED,
    MASTER72_GENERATED,
    MASTER72_PDF,
    RESOURCES,
    RESTRUCTED,
    RESTRUCTED_BOXEDCONTENT,
    RESTRUCTED_HEADLINES,
    RESTRUCTED_LISTS,
    RESTRUCTED_PAGENUMBERS,
    RESTRUCTED_PDF,
    RESTRUCTED_RESULT,
    RESTRUCTED_SECTIONS,
    RESTRUCTED_TEXT,
    RESTRUCTED_USERLINTING,
]
