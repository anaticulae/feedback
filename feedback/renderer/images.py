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
import os
import typing

import rawmaker.images.info
import utila

# TODO REPLCAE LATER
ImageInformations = typing.List[rawmaker.images.info.ImageInformation]

ZippedImageInfo = collections.namedtuple('ZippedImageInfo',
                                         'number, info, filename')
ZippedImageInfos = typing.List[ZippedImageInfo]


def load_image_informations(
        path: str,
        pages: tuple = None,
) -> ImageInformations:
    if not os.path.exists(path):
        return []

    files = utila.file_list(path, include='yaml')
    files = utila.files_sort(files)  # pylint:disable=R0204

    result = []
    for index, item in enumerate(files):
        source = os.path.join(path, item)
        loaded = rawmaker.images.info.load_info(source)
        if utila.should_skip(loaded.page, pages):
            continue
        result.append((index, loaded))  # TODO: CHECK INDEX WHEN SKIPPING PAGES
    return result


def load_images(path: str) -> list:
    if not os.path.exists(path):
        return []

    files = utila.file_list(path, include='yaml')
    files = utila.files_sort(files)  # pylint:disable=R0204

    result = []
    for item in files:
        source = os.path.join(path, item)
        loaded = utila.file_read_binary(source)
        filename = utila.file_name(item)
        fileext = utila.file_ext(item)
        result.append(((filename, fileext), loaded))
    return result


def images(path: str) -> list:
    if not os.path.exists(path):
        return []

    files = utila.file_list(path, include='yaml')
    files = utila.files_sort(files)  # pylint:disable=R0204

    result = [utila.file_name(item) for item in files]
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
