# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider.cli
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

from feedback import PACKAGE
from feedback import ROOT
from feedback import __version__
from feedback.command.utils import outhtml

FEATURE_NAME = 'view'
DESCRIPTION = 'generate central result view'

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile(producer='sections', name='sections_result'),
            ResultFile(producer='words', name='words_result'),
            ResultFile(producer='words', name='headlines_headlines'),
            ResultFile(producer='words', name='list_list'),
            ResultFile(producer='words', name='boxed_boxed'),
            ResultFile(producer='groupme', name='pagenumbers_pagenumbers'),
            ResultFile(producer=decider.cli.PROCESS, name='titlepage_user'),
        ],
        (outhtml('result'),),
    )
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='feedback.report',
        name=PACKAGE,
        description=DESCRIPTION,
        version=__version__,
    )
