# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

from pytest import mark
from pytest import raises
from utila.test import run
from utila.test import skip_not_virtual

from feedback import ROOT
from feedback.command.statistica import TEXT_STATISTICS
from feedback.command.statistica import TOC_AND_CHAPTER
from feedback.command.statistica import WORD_STATISTICS
from feedback.command.statistica import main
from tests.statistica import SAMPLE_TEXT_STATISTICS
from tests.statistica import SAMPLE_TOC_AND_CHAPTER
from tests.statistica import SAMPLE_WORD_STATISTICS


@skip_not_virtual
def test_run_statistica():
    """Install and run --help to ensure basic function"""
    uninstall = 'pip uninstall feedback -y'
    install = 'python setup.py install && feedback_statistica --help'

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr


@mark.parametrize('command', [
    ['-h'],
    ['-v'],
])
def test_run_command(monkeypatch, command):
    """Run help and version and format command to reach basic test coverage"""

    result = None
    with raises(SystemExit) as result:
        run_statistica(monkeypatch, command)
    assert_success(result)


def test_run_generation(monkeypatch):

    # command = ['--%s' % TEXT_STATISTICS,
    pass


def run_statistica(monkeypatch, command):
    with monkeypatch.context() as context:
        context.setattr(sys, 'argv', ['feedback_statistica'] + command)
        result = main()
        return result


def assert_success(result):
    result = str(result)
    assert 'SystemExit: 0' in result, result
