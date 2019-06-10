# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import join

from utila import create_step
from utila import featurepack

from feedback import ROOT
from feedback import __version__
from feedback.features.fonts.ugly import work

PROCESS_NAME = 'feedback_decider_fonts'
FEATURE_NAME = 'iamugly_view'
DESCRIPTION = 'generate html view for ugly fonts'
WORKPLAN = [
    create_step(
        FEATURE_NAME,
        work,
        [
            ('decider_fonts_iamugly', 'ugly'),
            ('rawmaker', 'fonts_header'),
        ],
        (
            ('ugly', 'html'),
            ('used', 'html'),
            'error',
        ),
    )
]
FEATURE_PATH = join(ROOT, 'feedback/features/fonts')


def main():
    featurepack(
        workplan=WORKPLAN,
        feature_path=FEATURE_PATH,
        feature_package='feedback.features.fonts',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
