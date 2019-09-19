# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import decider
import protocol
import pytest

import feedback.linter.linter
import tests.resources


@pytest.fixture
def findings():
    restructured = tests.resources.GENERATED_RESTRUCTED

    userlinting = os.path.join(restructured, decider.USER_LINT_OUTPUT)
    assert os.path.exists(userlinting), str(userlinting)

    loaded = protocol.load_result(userlinting)
    assert loaded
    return loaded


def test_report_linter_group_bypage(findings):  # pylint:disable=W0621
    grouped = feedback.linter.linter.group_finding_bypage(findings)
    assert grouped


# @pytest.fixture(
#     params=[tests.resources.RESTRUCTED, tests.resources.PORTING_PYTHON3_PDF],
#     ids=["spam", "ham"])
# def a(request):
#     return request.param
