# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys
import webbrowser

import pytest
import utila

import feedback.renderer.html
import tests.resources


@pytest.fixture
def masterpage72():
    path = tests.resources.GENERATED_MASTER_PAGE72
    loaded = feedback.renderer.html.load(path)
    return loaded


def test_features_render_load(masterpage72):  # pylint:disable=W0621
    assert masterpage72


def test_features_render_firstpage(testdir, masterpage72):  # pylint:disable=W0621
    outpath = os.path.join(str(testdir), 'firstpage.html')
    firstpage = utila.select_page(masterpage72, 0)

    rendered = feedback.renderer.html.render_page(firstpage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    if tests.single_execution():
        webbrowser.open(outpath)
