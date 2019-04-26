# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import join

from utila import FAILURE
from utila import SUCCESS
from utila import Parameter
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

COMMANDS = [
    Parameter(
        longcut='--%s' % TOC_AND_CHAPTER,
        message='compressed output of `rawmaker`',
    ),
    Parameter(
        longcut='--%s' % TEXT_STATISTICS,
        message='analysed text from `groupme`',
    ),
    Parameter(
        longcut='--%s' % WORD_STATISTICS,
        message='list of words with occurence from `groupme`',
    ),
]


def path_from_args(args):
    # TODO: CONVERT TO ABSOULTE PATH
    tocandchapter = args[TOC_AND_CHAPTER]
    textstatistics = args[TEXT_STATISTICS]
    wordstatistics = args[WORD_STATISTICS]
    return tocandchapter, textstatistics, wordstatistics


NEWLINE = '-------------------------------------------------------------------'


@saveme
def main():
    parser = create_parser(
        COMMANDS,
        version=__version__,
        inputparameter=False,
        outputparameter=True,
        prog='feedback_statistica',
        description='create html output for chapter analysis and word count.',
    )
    args = parse(parser)
    if not any(args.values()):
        # Missing parameter must procdue failure
        parser.print_help()
        return FAILURE

    _, output_path = sources(args)

    chapter, text, word = path_from_args(args)
    if not all([chapter, text, word]):
        logging_error('Missing resources')
        logging_error('chapter : %s ' % chapter)
        logging_error('text:     %s ' % text)
        logging_error('word:     %s ' % word)
        # Missing parameter must procdue failure
        return FAILURE
    write_to_stdout = not output_path
    try:
        result_chapter, result_words = generate(chapter, text, word)

        if write_to_stdout:
            logging(result_chapter)
            logging(NEWLINE)
            logging(result_words)
        else:
            makedirs(output_path, exist_ok=True)
            logging('write result to: %s' % output_path)
            file_append(
                join(output_path, 'chapter.html'),
                result_chapter,
                create=True,
            )
            file_append(
                join(output_path, 'words.html'),
                result_words,
                create=True,
            )
    except Exception as error:
        logging_error(error)
        logging_stacktrace()
        return FAILURE
    return SUCCESS
