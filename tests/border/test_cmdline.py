# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir

from utila import SUCCESS
from utila import run
from utila import run_command
from utila import skip_nonvirtual

from feedback import ROOT
from feedback.command.decider.border import PROCESS_NAME
from feedback.command.decider.border import main
from tests.border import HITS


@skip_nonvirtual
def test_run_decider_border():
    """Install and run --help to ensure basic function"""
    uninstall = 'pip uninstall feedback -y'
    install = 'python setup.py install && %s --help' % PROCESS_NAME

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=ROOT)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr


# pylint:disable=unused-argument
def test_run_main(testdir, monkeypatch):
    cmd = ['-i', HITS, '-o', '.']

    run_command(
        cmd,
        monkeypatch=monkeypatch,
        process=PROCESS_NAME,
        main=main,
        success=True)

    written_files = listdir('.')
    view_and_error_file = 2
    assert len(written_files) == view_and_error_file, str(written_files)
