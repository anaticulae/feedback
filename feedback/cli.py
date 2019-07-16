# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import featurepack

from feedback import PACKAGE_NAME
from feedback import ROOT
from feedback import __version__

DESCRIPTION = 'generate central result view'

WORKPLAN = []


def main():
    featurepack(
        workplan=WORKPLAN,
        root=ROOT,
        featurepackage='feedback.report',
        name=PACKAGE_NAME,
        description=DESCRIPTION,
        version=__version__,
    )
