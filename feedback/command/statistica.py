# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import exists
from os.path import join

from utila import FAILURE
from utila import SUCCESS
from utila import create_parser
from utila import file_append
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila import parse
from utila import saveme
from utila import sources

from feedback import __version__
from feedback.features.statistica.result import generate

TOC_AND_CHAPTER = 'toc_and_chapter'
TEXT_STATISTICS = 'text_statistics'
WORD_STATISTICS = 'word_statistics'

PROCESS_NAME = 'feedback_statistica'


@saveme
def main():
    parser = create_parser(
        version=__version__,
        inputparameter=True,
        outputparameter=True,
        prog='feedback_statistica',
        description='create html output for chapter analysis and word count.',
    )
    args = parse(parser)
    inputpath, outputpath = sources(args)

    if not inputpath or not outputpath:
        logging_error('Missing input or output')
        return FAILURE

    text_statistic = join(inputpath,
                          'analysis_statistica__statistics_chapters.yaml')
    words = join(inputpath, 'analysis_statistica__statistics_words.yaml')
    rawtexts = join(inputpath, 'groupme__chapter.yaml')

    ret = 0
    for item in [text_statistic, words, rawtexts]:
        if not exists(item):
            logging_error('File does not exist: %s' % item)
            ret += 1
    if ret:
        return ret

    try:
        result_chapter, result_words = generate(rawtexts, words, text_statistic)

        makedirs(outputpath, exist_ok=True)
        logging('write result to: %s' % outputpath)
        file_append(
            join(outputpath, '%s_chapter.html' % PROCESS_NAME),
            result_chapter,
            create=True,
        )
        file_append(
            join(outputpath, '%s_words.html' % PROCESS_NAME),
            result_words,
            create=True,
        )
    except Exception as error:  #pylint: disable=broad-except
        logging_error(error)
        logging_stacktrace()
        return FAILURE
    return SUCCESS
