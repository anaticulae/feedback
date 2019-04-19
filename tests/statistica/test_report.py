# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join
from tests.statistica import SAMPLE_ALPHA
from tests.statistica import SAMPLE_MEASURE
from tests.statistica import SAMPLE_OCCURENCE

from utila import file_read

from feedback.features.statistica.result import generate


def test_generate_chapter_report(tmpdir):
    source = [SAMPLE_ALPHA, SAMPLE_MEASURE, SAMPLE_OCCURENCE]

    report = join(tmpdir, 'report.html')

    generate(source, report)

    assert exists(report)
    assert len(file_read(report)) > 500
