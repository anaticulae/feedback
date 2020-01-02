# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Place experimental implementation here, before moving them to utila"""

from utila import ResultFile as RF

ResultFile = lambda producer, name: RF(producer=producer, name=name)


def infile(progress: str, stepfile: str):
    return (progress, stepfile)


def outhtml(name: str):
    return (name, 'html')


def outyaml(name: str):
    return (name, 'yaml')
