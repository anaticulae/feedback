# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import create_step as step
from utila import featurepack

from feedback import ROOT
from feedback import __version__
from feedback.command.utils import ResultFile
from feedback.command.utils import outhtml

TOC_AND_CHAPTER = 'toc_and_chapter'
TEXT_STATISTICS = 'text_statistics'
WORD_STATISTICS = 'word_statistics'

PROCESS_NAME = 'feedback_statistica'
FEATURE_NAME = 'feedback_statistica'

DESCRIPTION = 'create html output for chapter analysis and word count.'

CHAPTER = 'chapter'
WORDS = 'words'

WORKPLAN = [
    step(
        FEATURE_NAME,
        [
            ResultFile('groupme', 'chapter_chapter'),
            ResultFile('analysis_statistica', 'statistics_words'),
            ResultFile('analysis_statistica', 'statistics_chapters'),
        ],
        (
            outhtml(CHAPTER),
            outhtml(WORDS),
        ),
    )
]

CHAPTER_HTML = '%s__%s_%s' % (PROCESS_NAME, FEATURE_NAME, CHAPTER)
WORDS_HTML = '%s__%s_%s' % (PROCESS_NAME, FEATURE_NAME, WORDS)


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='feedback.features.statistica',
        name=PROCESS_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
