# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir

from utila import install_and_run
from utila import run_command
from utila import skip_nonvirtual

from feedback import PACKAGE_NAME
from feedback import ROOT
from feedback.cli import main
from tests.resources import RESTRUCTED


@skip_nonvirtual
def test_run_decider_border():
    """Install and run --help to ensure basic function"""
    install_and_run(
        ROOT,
        package=PACKAGE_NAME,
        executable=PACKAGE_NAME,
    )


# pylint:disable=unused-argument
def test_run_feedback(testdir, monkeypatch):
    cmd = ['-i', RESTRUCTED, '-o', '.']

    run_command(
        cmd,
        monkeypatch=monkeypatch,
        process=PACKAGE_NAME,
        main=main,
        success=False,  # TODO: change after adding functionality
    )
