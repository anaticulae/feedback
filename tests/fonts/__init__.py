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

FONTS_TDATA = join(TEST_PATH, 'fonts/data/')
assert exists(FONTS_TDATA), FONTS_TDATA

FONTS_UGLY_DATA = join(FONTS_TDATA, 'ugly')
assert exists(FONTS_UGLY_DATA), FONTS_UGLY_DATA
