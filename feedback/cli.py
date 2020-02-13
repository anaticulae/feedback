# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

import feedback
from feedback.command.utils import outhtml

FEATURE_NAME = 'problems'
DESCRIPTION = 'generate central result view'

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile(producer='sections', name='section_result'),
            ResultFile(producer='words', name='word_result'),
            ResultFile(producer='words', name='headlines_headlines'),
            ResultFile(producer='words', name='list_list'),
            ResultFile(producer='words', name='boxed_boxed'),
            ResultFile(producer='groupme', name='pagenumbers_pagenumbers'),
            ResultFile(producer=decider.PROCESS, name='titlepage_user'),
        ],
        (outhtml('result'),),
    ),
    step(
        'view',
        [
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
        ],
        (outhtml('pages/*'),),
    ),
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=feedback.ROOT,
        featurepackage='feedback.features.problems',
        name=feedback.PROCESS,
        description=DESCRIPTION,
        version=feedback.__version__,
    )
