#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import contextlib
import os

import german
import protocol

__version__ = '1.1.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PACKAGE = 'feedback'
PROCESS = 'feedback'


# TODO: REMOVE AFTER UPGRADING
def filter_mark(items: protocol.Findings, shortcut: str) -> protocol.Findings:
    """Filter `Findings` by shortcut and sort them by `location.value`
    afterwards.

    Args:
        items(protocol.Findings): list of findings
        shortcut(str): shortcut of finding.location, w word, p page,
                       ol oneline, etc.
    Returns:
        filtered, sorted list of `Findings`
    """
    assert all([item.location for item in items]), f'require location: {items}'
    selected = []
    for item in items:
        with contextlib.suppress(AttributeError):
            if item.location.shortcut == shortcut:
                selected.append(item)

    def line_key(item):
        # TODO: REMOVE LATER
        try:
            return item.location.value
        except AttributeError:
            return item.location.line

    items = sorted(selected, key=line_key)
    return items


protocol.filter_mark = filter_mark


def words(items: protocol.Findings) -> protocol.Findings:
    return filter_mark(items, shortcut='w')


protocol.words = words


def lines(items: protocol.Findings) -> protocol.Findings:
    return filter_mark(items, shortcut='ol')


protocol.lines = lines


def sentences(items: protocol.Findings) -> protocol.Findings:
    return filter_mark(items, shortcut='s')


protocol.sentences = sentences


def split_token(text: str, normalize: bool = True):
    # replace text division -
    text = text.replace('-\n', '')
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    if normalize:
        tokens = [token for token in tokens if token]
    return tokens


# TODO: REMOVE AFTER UPGRADING GERMAN
german.split_token = split_token
