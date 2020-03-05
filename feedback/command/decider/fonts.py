# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
from utila import create_step as step
from utila import featurepack

from feedback import ROOT
from feedback import __version__
from feedback.command.utils import ResultFile
from feedback.command.utils import outhtml
from feedback.command.utils import outyaml

PROCESS_NAME = 'feedback_decider_fonts'
FEATURE_NAME = 'iamugly_view'
DESCRIPTION = 'generate html view for ugly fonts'
WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile('decider_fonts', 'ugly_ugly'),
            ResultFile('rawmaker', 'fonts_header'),
        ],
        (
            outhtml('ugly'),
            outhtml('used'),
            outyaml('error'),
        ),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='feedback.features.fonts',
        config=utila.FeaturePackConfig(
            name=PROCESS_NAME,
            description=DESCRIPTION,
            version=__version__,
        ),
    )
