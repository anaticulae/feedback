# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import feedback

RESOURCES = os.path.join(feedback.ROOT, 'tests/resources')

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
MASTER = os.path.join(RESOURCES, 'master')

GENERATED = os.path.join(RESOURCES, 'generated')

RESTRUCTED_PDF = os.path.join(DOCU, 'restructuredtext.pdf')
PORTING_PYTHON3_PDF = os.path.join(DOCU, 'porting_extension_modules.pdf')
MASTER72_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

LEFTRIGHT = os.path.join(BOOK, 'leftright.pdf')
LEFTRIGHT_GENERATED = os.path.join(GENERATED, 'book_leftright')

BACHELOR56 = os.path.join(GENERATED, 'bachelor_page_56_hard_to_read')
BACHELOR56_PDF = os.path.join(BACHELOR, 'page_56_hard_to_read.pdf')

BACHELOR90 = os.path.join(GENERATED, 'bachelor_bachelor90')
BACHELOR90_PDF = os.path.join(BACHELOR, 'bachelor90.pdf')

MASTER116 = os.path.join(GENERATED, 'master_page_116_images_toc_formular')
MASTER116_PDF = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

MASTER72_GENERATED = os.path.join(GENERATED, 'master_page_72_noimages_toc')

GENERATED_PORTING_PYTHON3 = os.path.join(GENERATED, 'docu_porting_extension_modules') # yapf:disable

# test after running generation step in update.py
REQUIRED_RESOURCES = [
    BACHELOR,
    BACHELOR56,
    BACHELOR56_PDF,
    BACHELOR90,
    BACHELOR90_PDF,
    GENERATED,
    GENERATED_PORTING_PYTHON3,
    LEFTRIGHT,
    LEFTRIGHT_GENERATED,
    MASTER116,
    MASTER116_PDF,
    MASTER72_GENERATED,
    MASTER72_PDF,
    RESOURCES,
    RESTRUCTED_PDF,
]
