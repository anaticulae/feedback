# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import SUCCESS
from utila import saveme
from utila.cmdline import create_parser

from feedback import __version__

COMMANDS = []  # add additonal commands here


@saveme
def main():
    parser = create_parser(
        COMMANDS,
        version=__version__,
        outputparameter=True,
        inputparameter=True,
    )

    parser.print_help()

    return SUCCESS
