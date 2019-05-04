# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from feedback.features.statistica.result import generate
from tests.statistica import SAMPLE_GROUPME_TEXT
from tests.statistica import SAMPLE_TEXT_STATISTICS
from tests.statistica import SAMPLE_WORD_STATISTICS


def test_generate_chapter_report():
    chapter, word = generate(
        SAMPLE_GROUPME_TEXT,
        SAMPLE_WORD_STATISTICS,
        SAMPLE_TEXT_STATISTICS,
    )

    assert len(chapter) > 500
    assert len(word) > 200
