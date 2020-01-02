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
from iamraw import BoundingBox

import feedback.features.problems.renderer
import tests
import tests.feedback


def test_report_view_work(testdir):
    """Generate report view and open in current webbrowser if test is
    specified as single test via pytest -k .."""
    root = str(testdir)

    sections = tests.resources.RESTRUCTED_SECTIONS
    text = tests.resources.RESTRUCTED_RESULT
    headlines = tests.resources.RESTRUCTED_HEADLINES
    boxed = tests.resources.RESTRUCTED_BOXEDCONTENT
    lists = tests.resources.RESTRUCTED_LISTS
    pagenumbers = tests.resources.RESTRUCTED_PAGENUMBERS
    problems = tests.resources.RESTRUCTED_USERLINTING

    result = feedback.features.problems.renderer.work(
        sections,
        text,
        headlines,
        lists,
        boxed,
        pagenumbers,
        problems,
    )

    outpath = os.path.join(root, 'result.html')
    utila.file_create(outpath, result)

    if tests.single_execution():
        # Hint: Enable for fast feedback loop
        webbrowser.open(outpath)


@pytest.fixture(
    params=[
        tests.resources.GENERATED_RESTRUCTED,
        tests.resources.GENERATED_PORTING_PYTHON3,
        tests.resources.GENERATED_MASTER_PAGE72,
    ],
    ids=[
        utila.make_single(tests.resources.GENERATED_RESTRUCTED),
        utila.make_single(tests.resources.GENERATED_PORTING_PYTHON3),
        utila.make_single(tests.resources.GENERATED_MASTER_PAGE72),
    ])
def feedback_result(request):
    return request.param


def test_report_view_main(feedback_result, testdir, monkeypatch): # pylint:disable=W0621
    inpath = feedback_result
    root = str(testdir)
    tests.feedback.run(f'-i {inpath} -o {root}', monkeypatch=monkeypatch)


def test_find_bounding_box():
    data = [(9, [
        (0, 0, [
            [
                (BoundingBox(x0=68.61, y0=140.62, x1=543.39, y1=223.71),
                 (1, [(BoundingBox(x0=72.00, y0=143.40, x1=179.60, y1=152.80),
                       3, 'This is normal text.'),
                      (BoundingBox(x0=93.52, y0=165.32, x1=222.64, y1=174.72),
                       4, 'This is blockquoted text.'),
                      (BoundingBox(x0=93.52, y0=187.24, x1=340.99, y1=196.64),
                       5, 'This is another paragraph of'),
                      (BoundingBox(x0=115.04, y0=209.16, x1=281.81, y1=218.56),
                       6, 'This is a nested block of text.')])),
            ],
        ]),
        (0, 1, [
            [
                (BoundingBox(x0=68.61, y0=251.01, x1=543.39, y1=345.06),
                 (0, [(BoundingBox(x0=72.00, y0=252.70, x1=367.89, y1=339.90),
                       8, '<p>This is normal text.</p> </div>')])),
            ],
        ]),
    ])]
    find_boxed = feedback.features.problems.renderer.find_boxed
    assert find_boxed(data, 9, 1, 0) == 'This is normal text.'
    assert find_boxed(data, 9, 1, 1) == 'This is blockquoted text.'
    assert find_boxed(data, 9, 1, 2) == 'This is another paragraph of'

    assert find_boxed(data, 9, 0, 0) == '<p>This is normal text.</p> </div>'
