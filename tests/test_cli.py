# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import pytest
import utilo
import utilotest

import tests


def test_run_feedback_help(mp):
    """Ensure that installing process works correctly."""
    tests.run('--help', mp=mp)


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.BOOK007_PDF, id='leftright'),
    pytest.param(hoverpower.MASTER072_PDF, id='master72'),
])
def test_run_feedback_linter_findings_to_shape(source, td, mp):
    """Run linted example where findings are converted to shapes to
    display more information to the user."""
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    utilo.copy_content(
        source,
        td.tmpdir,
        pattern='(rawmaker|groupme|textflow|words|pagenumber)__*.yaml',
    )
    completed = utilo.run('decider_border')
    assert completed.returncode == utilo.SUCCESS, str(completed)
    # run feedback
    tests.run('--view', mp=mp)
    # open result
    first_file = td.tmpdir.join('feedback__view_pages/0.html')
    assert os.path.exists(first_file), str(first_file)
    with utilotest.open_webbrowser(first_file):
        pass


@pytest.mark.xfail(reason='software integration')
@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_run_feedback_view(td, mp):
    root = td.tmpdir
    source = hoverpower.link(hoverpower.BACHELOR056_PDF)
    cmd = f'--pdf {hoverpower.BACHELOR056_PDF} -i {source} -o {root} --pages=9'
    # run feedback
    tests.run(cmd, mp=mp)
    # TODO: RENAME TO 9 AFTER FIXING GENERATOR
    page9 = os.path.join(root, 'feedback__view_pages/0.html')
    with utilotest.open_webbrowser(page9):
        # ensure that word marks are set on page9
        content = utilo.file_read(page9)
        # counted = content.count('id="word9')
        # assert counted >= 20, counted
        counted = content.count('id="line9')
        assert counted >= 4, counted


@pytest.mark.xfail(reason='software integration')
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_feedback_plot(td, mp):
    source = hoverpower.link(hoverpower.MASTER072_PDF)
    cmd = f'-i {source} -o {td.tmpdir} --plot'
    # run feedback
    tests.run(cmd, mp=mp)
    assert 0
