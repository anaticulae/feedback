# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from utila import logging_error

from feedback import ROOT

TEST_PATH = join(ROOT, 'tests')
assert exists(TEST_PATH)


# TODO: remove after upgrading utila 0.6.3
def assert_file(files, filetype: str):
    """Ensure that the given `files` have the correct `filetype`

    Args:
        List[str]: list with files
        filetype(str): filetype without leading dot
    Returns:
        raises assertion when passing invalid files
    """
    # support passing single str
    files = [files] if isinstance(files, str) else files
    # ensure passing without dot
    filetype = filetype[1:] if filetype[0] == '.' else filetype
    raises = 0
    for item in files:
        if not item.endswith('.%s' % filetype):
            logging_error('No %s file: %s' % (filetype, item))
            raises += 1
    assert not raises, 'wrong file types'


def assert_html(files):
    """Ensure that all given `files` are `html` files"""
    assert_file(files, 'html')
