# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import webbrowser

import pytest
import utila

import feedback
import feedback.cli
import tests.feedback_
import tests.resources


# pylint:disable=unused-argument
def test_run_feedback(testdir, monkeypatch):
    cmd = ['-i', tests.resources.RESTRUCTED, '-o', '.']

    utila.run_command(
        cmd,
        monkeypatch=monkeypatch,
        process=feedback.PACKAGE,
        main=feedback.cli.main,
        success=True,
    )


def test_run_feedback_help():
    """Ensure that installing process works correctly."""
    completed = utila.run('feedback --help')
    assert completed.returncode == utila.SUCCESS, str(completed)


@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.LEFTRIGHT_GENERATED, id='leftright'),
    pytest.param(tests.resources.MASTER72_GENERATED, id='master72'),
])
def test_run_feedback_linter_findings_to_shape(source, testdir, monkeypatch):
    """Run linted example where findings are converted to shapes to
    display more information to the user."""
    root = str(testdir)
    # TODO: UNIT THIS PATTERN AFTER UPGRADING UTILA
    utila.copy_content(source, root, pattern='rawmaker__*.yaml')
    utila.copy_content(source, root, pattern='groupme__*.yaml')
    completed = utila.run('decider_border')
    assert completed.returncode == utila.SUCCESS, str(completed)

    tests.feedback_.run('--view', monkeypatch)

    first_file = os.path.join(root, 'feedback__view_pages/0.html')
    assert os.path.exists(first_file), str(first_file)

    if utila.single_execution():
        webbrowser.open(first_file)


def test_run_feedback_view(testdir, monkeypatch):
    root = testdir.tmpdir
    cmd = f'-i {tests.resources.LEFTRIGHT_GENERATED} -o .'

    utila.run_command(
        cmd,
        monkeypatch=monkeypatch,
        process=feedback.PACKAGE,
        main=feedback.cli.main,
        success=True,
    )

    first_file = os.path.join(root, 'feedback__view_pages/0.html')
    assert os.path.exists(first_file), str(first_file)
    if utila.single_execution():
        webbrowser.open(first_file)
