# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import feedback
import feedback.utils

FEATURE_NAME = 'problems'
DESCRIPTION = 'generate central result view'

WORKPLAN = [
    utilo.create_step(
        'view',
        [
            utilo.ResultFile('rawmaker', name='text_text'),
            utilo.ResultFile('rawmaker', name='text_positions'),
            utilo.ResultFile('rawmaker', name='oneline_text_text'),
            utilo.ResultFile('rawmaker', name='oneline_text_positions'),
            utilo.ResultFile('rawmaker', name='border_pages'),
            utilo.ResultFile('textflow', name='alignment_current'),
            utilo.ResultFile('rawmaker', name='fonts_header'),
            utilo.ResultFile('rawmaker', name='fonts_content'),
            utilo.Directory('rawmaker__images_images'),
            utilo.Directory('rawmaker__figures_figures'),
            utilo.ResultFile('rawmaker', name='boxes_boxes'),
            utilo.ResultFile('rawmaker', name='horizontals_horizontals'),
            utilo.ResultFile('rawmaker', name='line_line'),
            utilo.ResultFile('decider_border', name='detection_hits'),
            utilo.ResultFile('words', name='word_result'),
            utilo.ResultFile('sections', name='section_result'),
            utilo.ResultFile('groupme', name='footer_footerheader'),
            utilo.Directory('__optimized__'),
        ],
        (utilo.File('feedback__view_pages/*', ext='html'),),
    ),
    utilo.create_step(
        'images',
        [
            utilo.Directory('rawmaker__images_images'),
        ],
        (  # TODO: REPLACE THIS HACK LATER
            utilo.File('feedback__view_pages/{FILEHASH}', ext='???'),),
    ),
    utilo.create_step(
        'figures',
        [
            utilo.Directory('rawmaker__figures_figures'),
        ],
        (utilo.File('feedback__view_pages/{FILEHASHS}', ext='png'),),
    ),
    utilo.create_step(
        'findings',
        inputs=[
            utilo.ResultFile(producer='words', name='sentences_bounding'),
            utilo.Directory('__optimized__'),
            utilo.Value(name='pdf', typ=None, defaultvar=None),
        ],
    ),
    utilo.create_step(
        name='plot',
        inputs=[
            utilo.ResultFile(producer='groupme', name='pagenumbers_magic'),
            utilo.Directory('__optimized__'),
        ],
        output=[
            ('findings_histogram', 'png'),
            ('findings_types_pie', 'png'),
        ],
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=feedback.ROOT,
        featurepackage='feedback.features',
        config=utilo.FeaturePackConfig(
            name=feedback.PROCESS,
            description=DESCRIPTION,
            version=feedback.__version__,
            pages=True,
            multiprocessed=True,
        ),
    )
