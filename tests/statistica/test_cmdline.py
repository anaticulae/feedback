# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys
from os import listdir

from pytest import mark
from pytest import raises
from utila import SUCCESS
from utila.test import run
from utila.test import skip_not_virtual

from feedback import ROOT
from feedback.command.statistica import PROCESS_NAME
from feedback.command.statistica import main
from tests.statistica import STAT_SAMPLE_DATA


@skip_not_virtual
def test_run_statistica():
    """Install and run --help to ensure basic function"""
    uninstall = 'pip uninstall feedback -y'
    install = 'python setup.py install && %s --help' % PROCESS_NAME

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr


@mark.parametrize('command', [
    ['-h'],
    ['-v'],
])
def test_run_command(monkeypatch, command):
    """Run help and version and format command to reach basic test coverage"""
    result = run_statistica(command, monkeypatch)
    assert result


def test_run_generation_to_output(testdir, monkeypatch):  #pylint:disable=W0613
    outdir = 'result'
    cmd = ['-i', STAT_SAMPLE_DATA, '-o', 'result']

    run_statistica(cmd, monkeypatch)
    written_files = listdir(outdir)
    assert len(written_files) == 2, written_files


def run_statistica(command, monkeypatch, expect_success=True):
    result = None
    with raises(SystemExit) as result:
        with monkeypatch.context() as context:
            context.setattr(sys, 'argv', [PROCESS_NAME] + command)
            main()
    if expect_success:
        assert_success(result)
    else:
        assert_failure(result)
    return result


def assert_success(result):
    result = str(result)
    assert 'SystemExit: 0' in result, result


def assert_failure(result):
    result = str(result)
    assert 'SystemExit: 1' in result, result
