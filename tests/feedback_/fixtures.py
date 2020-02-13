# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pytest

import feedback.renderer.html
import tests.resources


@pytest.fixture
def masterpage72():
    path = tests.resources.MASTER72_GENERATED
    loaded = feedback.renderer.html.from_path(path)
    return loaded


@pytest.fixture
def leftright():
    path = tests.resources.LEFTRIGHT_GENERATED
    loaded = feedback.renderer.html.from_path(path)
    return loaded
