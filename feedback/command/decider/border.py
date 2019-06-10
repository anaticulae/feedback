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
from feedback.command.utils import infile
from feedback.command.utils import outhtml
from feedback.command.utils import outyaml
from feedback.features.border.hitthebox import work

PROCESS_NAME = 'feedback_decider_border'
FEATURE_NAME = 'hitthebox_view'
DESCRIPTION = 'generate html view for overlapping content'
WORKPLAN = [
    create_step(FEATURE_NAME, work, [
        infile('decider_border_hitthebox', 'hits'),
    ], (
        outhtml('result'),
        outyaml('error'),
    ))
]
FEATURE_PATH = join(ROOT, 'feedback/features/border')


def main():
    featurepack(
        workplan=WORKPLAN,
        feature_path=FEATURE_PATH,
        feature_package='feedback.features.border',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
