# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import feedback
import feedback.utils

FEATURE_NAME = 'problems'
DESCRIPTION = 'generate central result view'

WORKPLAN = [
    utila.create_step(
        'view',
        [
            utila.ResultFile('rawmaker', name='text_text'),
            utila.ResultFile('rawmaker', name='text_positions'),
            utila.ResultFile('rawmaker', name='oneline_text_text'),
            utila.ResultFile('rawmaker', name='oneline_text_positions'),
            utila.ResultFile('rawmaker', name='border_pages'),
            utila.ResultFile('textflow', name='alignment_current'),
            utila.ResultFile('rawmaker', name='fonts_header'),
            utila.ResultFile('rawmaker', name='fonts_content'),
            utila.Directory('rawmaker__images_images'),
            utila.Directory('rawmaker__figures_figures'),
            utila.ResultFile('rawmaker', name='boxes_boxes'),
            utila.ResultFile('rawmaker', name='horizontals_horizontals'),
            utila.ResultFile('rawmaker', name='line_line'),
            utila.ResultFile('decider_border', name='detection_hits'),
            utila.ResultFile('words', name='word_result'),
            utila.ResultFile('sections', name='section_result'),
            utila.ResultFile('groupme', name='footer_footerheader'),
            utila.Directory('__optimized__'),
        ],
        (utila.File('feedback__view_pages/*', ext='html'),),
    ),
    utila.create_step(
        'images',
        [
            utila.Directory('rawmaker__images_images'),
        ],
        (  # TODO: REPLACE THIS HACK LATER
            utila.File('feedback__view_pages/{FILEHASH}', ext='???'),),
    ),
    utila.create_step(
        'figures',
        [
            utila.Directory('rawmaker__figures_figures'),
        ],
        (utila.File('feedback__view_pages/{FILEHASHS}', ext='png'),),
    ),
    utila.create_step(
        'findings',
        inputs=[
            utila.ResultFile(producer='words', name='sentences_bounding'),
            utila.Directory('__optimized__'),
            utila.Value(name='pdf', typ=None, defaultvar=None),
        ],
    ),
    utila.create_step(
        name='plot',
        inputs=[
            utila.ResultFile(producer='groupme', name='pagenumbers_magic'),
            utila.Directory('__optimized__'),
        ],
        output=[
            ('findings_histogram', 'png'),
            ('findings_types_pie', 'png'),
        ],
    ),
]


def main():
    utila.featurepack(
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
