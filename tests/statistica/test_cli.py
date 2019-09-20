# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir

import pytest
import utila

from feedback import PACKAGE
from feedback import ROOT
from feedback.command.statistica import PROCESS_NAME
from feedback.command.statistica import main
from tests import assert_html
from tests.statistica import STAT_SAMPLE_DATA


@utila.skip_nonvirtual
def test_install_and_run_statistica():
    """Install and run --help to ensure basic function"""
    utila.install_and_run(
        ROOT,
        package=PACKAGE,
        executable=PROCESS_NAME,
    )


@pytest.mark.parametrize('command', [
    ['-h'],
    ['-v'],
])
def test_run_command(monkeypatch, command):
    """Run help and version and format command to reach basic test coverage"""
    run_statistica(command, monkeypatch)


def test_run_generation_to_output(testdir, monkeypatch):  #pylint:disable=W0613
    outdir = 'result'
    cmd = ['-i', STAT_SAMPLE_DATA, '-o', 'result']

    run_statistica(cmd, monkeypatch)
    written_files = listdir(outdir)
    assert len(written_files) == 2, written_files

    assert_html(written_files)


def run_statistica(command, monkeypatch, success=True):
    utila.run_command(
        command,
        PROCESS_NAME,
        main,
        success=success,
        monkeypatch=monkeypatch,
    )
