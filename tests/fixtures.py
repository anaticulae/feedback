# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import feedback.renderer.loader


@pytest.fixture
def masterpage72():
    path = hoverpower.link(hoverpower.MASTER072_PDF)
    utilotest.fixture_requires(path)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded


@pytest.fixture
def bachelor128page10():
    path = hoverpower.link(hoverpower.BACHELOR128_PDF)
    utilotest.fixture_requires(path)
    loaded = feedback.renderer.loader.from_path(path, pages=10)
    return loaded


@pytest.fixture
def leftright():
    path = hoverpower.link(hoverpower.BOOK007_PDF)
    utilotest.fixture_requires(path)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded


@pytest.fixture
def bachelor56():
    path = hoverpower.link(hoverpower.BACHELOR056_PDF)
    utilotest.fixture_requires(path)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded


@pytest.fixture
def master116():
    path = hoverpower.link(hoverpower.MASTER116_PDF)
    utilotest.fixture_requires(path)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded
