# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import webbrowser

import power
import pytest
import utila
import utilatest

import feedback
import feedback.cli
import tests.feedback_


def test_run_feedback_help():
    """Ensure that installing process works correctly."""
    completed = utila.run('feedback --help')
    assert completed.returncode == utila.SUCCESS, str(completed)


@pytest.mark.parametrize('source', [
    pytest.param(power.link(power.BOOK007_PDF), id='leftright'),
    pytest.param(power.link(power.MASTER072_PDF), id='master72'),
])
@utilatest.requires(power.BOOK007_PDF)
@utilatest.requires(power.MASTER072_PDF)
def test_run_feedback_linter_findings_to_shape(source, testdir, monkeypatch):
    """Run linted example where findings are converted to shapes to
    display more information to the user."""
    root = str(testdir)
    utila.copy_content(
        source,
        root,
        pattern='(rawmaker|groupme|textflow|words)__*.yaml',
    )
    completed = utila.run('decider_border')
    assert completed.returncode == utila.SUCCESS, str(completed)

    tests.feedback_.run('--view', monkeypatch=monkeypatch)

    first_file = os.path.join(root, 'feedback__view_pages/0.html')
    assert os.path.exists(first_file), str(first_file)

    if utilatest.single_execution():
        webbrowser.open(first_file)


@pytest.mark.xfail(reason='broken data generator')
@utilatest.requires(power.BACHELOR056_PDF)
def test_run_feedback_view(testdir, monkeypatch):
    root = testdir.tmpdir
    cmd = f'-i {power.link(power.BACHELOR056_PDF)} -o {root} --pages=9'

    with utila.chdir(power.link(power.BACHELOR056_PDF)):
        utilatest.run_command(
            cmd,
            monkeypatch=monkeypatch,
            process=feedback.PACKAGE,
            main=feedback.cli.main,
            success=True,
        )

    # TODO: RENAME TO 9 AFTER FIXING GENERATOR
    page9 = os.path.join(root, 'feedback__view_pages/0.html')
    assert os.path.exists(page9), str(page9)

    # ensure that word marks are set on page9
    content = utila.file_read(page9)
    counted = content.count('id="word9')
    assert counted >= 20, counted

    if utilatest.single_execution():
        webbrowser.open(page9)
