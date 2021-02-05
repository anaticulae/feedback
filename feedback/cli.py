# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
from utila import Pattern
from utila import ResultFile
from utila import create_step as step
from utila import featurepack

import feedback
import feedback.utils

FEATURE_NAME = 'problems'
DESCRIPTION = 'generate central result view'

WORKPLAN = [
    step(
        'view',
        [
            ResultFile(producer='rawmaker', name='text_text'),
            ResultFile(producer='rawmaker', name='text_positions'),
            ResultFile(producer='rawmaker', name='oneline_text_text'),
            ResultFile(producer='rawmaker', name='oneline_text_positions'),
            ResultFile(producer='rawmaker', name='border_pages'),
            ResultFile(producer='textflow', name='alignment_current'),
            ResultFile(producer='rawmaker', name='fonts_header'),
            ResultFile(producer='rawmaker', name='fonts_content'),
            utila.Directory('rawmaker__images_images'),
            utila.Directory('rawmaker__figures_figures'),
            ResultFile(producer='rawmaker', name='boxes_boxes'),
            ResultFile(producer='rawmaker', name='horizontals_horizontals'),
            ResultFile(producer='rawmaker', name='line_line'),
            ResultFile(producer='decider_border', name='detection_hits'),
            ResultFile(producer='words', name='word_result'),
            ResultFile(producer='sections', name='section_result'),
            ResultFile(producer='groupme', name='footer_footerheader'),
            Pattern(name='*_user', ext='yaml'),
        ],
        (utila.File('feedback__view_pages/*', ext='html'),),
    ),
    step(
        'images',
        [
            utila.Directory('rawmaker__images_images'),
        ],
        (  # TODO: REPLACE THIS HACK LATER
            utila.File('feedback__view_pages/{FILEHASH}', ext='???'),),
    ),
    step(
        'figures',
        [
            utila.Directory('rawmaker__figures_figures'),
        ],
        (utila.File('feedback__view_pages/{FILEHASHS}', ext='png'),),
    ),
    utila.create_step(
        name='plot',
        inputs=[
            ResultFile(producer='rawmaker', name='border_pages'),
            Pattern(name='*_user', ext='yaml'),
        ],
        output=[
            ('findings_histogram', 'png'),
        ],
    ),
]


def main():
    featurepack(
        workplan=WORKPLAN,
        root=feedback.ROOT,
        featurepackage='feedback.features',
        config=utila.FeaturePackConfig(
            name=feedback.PROCESS,
            description=DESCRIPTION,
            version=feedback.__version__,
            pages=True,
            multiprocessed=True,
        ),
    )
