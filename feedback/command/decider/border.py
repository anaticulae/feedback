# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import ResultFile
from utila import create_step as step
from utila import featurepack

from feedback import ROOT
from feedback import __version__
from feedback.command.utils import outhtml
from feedback.command.utils import outyaml

PROCESS_NAME = 'feedback_decider_border'
FEATURE_NAME = 'hitthebox'
DESCRIPTION = 'generate html view for overlapping content'

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile(producer='decider_border_hitthebox', name='hits'),
        ],
        (
            outhtml('result'),
            outyaml('error'),
        ),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='feedback.features.border',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
