# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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
from feedback.features.statistica.result import work

TOC_AND_CHAPTER = 'toc_and_chapter'
TEXT_STATISTICS = 'text_statistics'
WORD_STATISTICS = 'word_statistics'

PROCESS_NAME = 'feedback_statistica'
FEATURE_NAME = 'feedback_statistica'

DESCRIPTION = 'create html output for chapter analysis and word count.'
WORKPLAN = [
    create_step(FEATURE_NAME, work, [
        infile('groupme', 'chapter'),
        infile('analysis_statistica', 'statistics_words'),
        infile('analysis_statistica', 'statistics_chapters'),
    ], (
        outhtml('chapter'),
        outhtml('words'),
    ))
]

FEATURE_PATH = join(ROOT, 'feedback/features/statistica')


def main():
    featurepack(
        workplan=WORKPLAN,
        feature_path=FEATURE_PATH,
        feature_package='feedback.features.statistica',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
