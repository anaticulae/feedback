#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import configo

__version__ = '1.15.2'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'feedback'

configo.cloud_lookup(PROCESS)
