# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module aims to manage extracted images to prepare them for
printing.
"""

import collections
import glob
import os
import typing

# TODO: REPLACE WITH UTILA CODE
import rawmaker.images.info
import utila

ImageInformations = typing.List[rawmaker.images.info.ImageInformation]

ZippedImageInfo = collections.namedtuple('ZippedImageInfo',
                                         'number, info, filename')
ZippedImageInfos = typing.List[ZippedImageInfo]

# TODO: VERY COMPLEX, REFACTOR


def load_image_informations(
        path: str,
        pages: tuple = None,
) -> ImageInformations:
    if not os.path.exists(path):
        return []
    result = []
    # TODO: REPLACE WITH UTILA CODE
    with utila.chdir(path):
        files = glob.glob('*.yaml')
        for index, item in enumerate(sorted(files, key=number)):
            source = os.path.join(path, item)
            loaded = rawmaker.images.info.load_info(source)
            if utila.should_skip(loaded.page, pages):
                continue
            result.append((index, loaded))
    return result


def load_images(path: str) -> list:
    if not os.path.exists(path):
        return []
    result = []
    # TODO: REPLACE WITH UTILA CODE
    with utila.chdir(path):
        files = os.scandir(path)
        # TODO: REPLACE WITH UTILA SORT METHOD
        for item in sorted(files, key=lambda x: number(x.name)):
            if item.name.endswith('.yaml'):
                continue
            source = os.path.join(path, item)
            loaded = utila.file_read_binary(source)
            result.append((item.name, loaded))
    return result


def images(path: str) -> list:
    if not os.path.exists(path):
        return []
    result = []
    # TODO: REPLACE WITH UTILA CODE
    with utila.chdir(path):
        files = os.scandir(path)
        # TODO: REPLACE WITH UTILA SORT METHOD
        for item in sorted(files, key=lambda x: number(x.name)):
            if item.name.endswith('.yaml'):
                continue
            result.append(item.name)
    return result


def zip_images(path: str, pages: tuple = None) -> ZippedImageInfos:
    img = images(path)
    informations = load_image_informations(path, pages)
    result = []
    for index, info in informations:
        result.append(ZippedImageInfo(index, info, img[index]))
    return result


def select_images(items, page):
    if not items:
        return []
    return [item for item in items if item[1].page == page]


def number(item: str) -> int:
    return int(item.split('.')[0])
