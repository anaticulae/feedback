# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import tests.feedback_.renderer as tfr
from tests.feedback_.fixtures import master116  # pylint:disable=W0611


def test_renderer_select_source_master116_toc(tmpdir, master116):  # pylint:disable=W0621
    """Ensure that toc lines are printed justifieded and as a result of
    this, the dots are printed over the whole line."""
    page = 4
    with tfr.render_and_open(
            tmpdir,
            master116,
            page=page,
    ) as source:

        toc_lines = source.count('text-align-last:justify')
        assert toc_lines >= 30, toc_lines
