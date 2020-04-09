# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider
import utila
from utila import Pattern
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

import feedback
import feedback.utils
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
            utila.Directory('rawmaker__images_images'),
            ResultFile(producer='rawmaker', name='boxes_boxes'),
            ResultFile(producer='decider_border', name='detection_hits'),
            Pattern(name='*_user', ext='yaml'),
        ],
        (outhtml('pages/*'),),
    ),
    step(
        'images',
        [
            utila.Directory('rawmaker__images_images'),
        ],
        (utila.File('feedback__view_pages/*', ext='???'),),
    ),
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=feedback.ROOT,
        featurepackage='feedback.features.problems',
        config=utila.FeaturePackConfig(
            name=feedback.PROCESS,
            description=DESCRIPTION,
            version=feedback.__version__,
        ),
    )
