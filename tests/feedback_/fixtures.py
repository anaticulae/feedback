# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest

import feedback.renderer.loader


@pytest.fixture
def masterpage72():
    path = power.link(power.MASTER072_PDF)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded


@pytest.fixture
def leftright():
    path = power.link(power.BOOK007_PDF)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded


@pytest.fixture
def bachelor56():
    path = power.link(power.BACHELOR056_PDF)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded


@pytest.fixture
def master116():
    path = power.link(power.MASTER116_PDF)
    loaded = feedback.renderer.loader.from_path(path)
    return loaded
