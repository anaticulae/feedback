# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
from iamraw import BoundingBox

from feedback.report.view import find_boxed
from feedback.report.view import work
from tests.resources import RESTRUCTED_BOXEDCONTENT
from tests.resources import RESTRUCTED_HEADLINES
from tests.resources import RESTRUCTED_LISTS
from tests.resources import RESTRUCTED_PAGENUMBERS
from tests.resources import RESTRUCTED_RESULT
from tests.resources import RESTRUCTED_SECTIONS


def test_report_view_work(testdir):
    root = str(testdir)

    sections = RESTRUCTED_SECTIONS
    text = RESTRUCTED_RESULT
    headlines = RESTRUCTED_HEADLINES
    boxed = RESTRUCTED_BOXEDCONTENT
    lists = RESTRUCTED_LISTS
    pagenumbers = RESTRUCTED_PAGENUMBERS

    result = work(
        sections,
        text,
        headlines,
        lists,
        boxed,
        pagenumbers,
    )

    outpath = os.path.join(root, 'result.html')
    utila.file_create(outpath, result)

    # TODO: Detect if developer uses bttv or use pytest-env vars, to
    # avoid commenting in/out.
    # Hint: Enable for fast feedback loop
    # import webbrowser
    # webbrowser.open(outpath)

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

    assert find_boxed(data, 9, 1, 0) == 'This is normal text.'
    assert find_boxed(data, 9, 1, 1) == 'This is blockquoted text.'
    assert find_boxed(data, 9, 1, 2) == 'This is another paragraph of'

    assert find_boxed(data, 9, 0, 0) == '<p>This is normal text.</p> </div>'
