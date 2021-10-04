# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This module aims to manage extracted images to prepare them for
printing.
"""

import collections
import dataclasses
import os
import typing

import iamraw
import serializeraw
import utila

ZippedImageInfo = collections.namedtuple(
    'ZippedImageInfo',
    'info, filename',
)
ZippedImageInfos = typing.List[ZippedImageInfo]


@dataclasses.dataclass
class RawImage:
    name: str = None
    ext: str = None
    raw: bytes = None


RawImages = typing.List[RawImage]


def load_image_informations(
    path: str,
    pages: tuple = None,
) -> iamraw.ImageInformations:
    if not os.path.exists(path):
        return []
    loaded = serializeraw.load_image_infos_frompath(
        path,
        pages=pages,
        skip_hidden=True,
    )
    result = utila.flatten_content(loaded)
    return result


IMAGE_EXT = ['png', 'jpg', 'jpeg']


def load_images(path: str, pages: tuple = None) -> RawImages:
    if not os.path.exists(path):
        return []
    informations = load_image_informations(path, pages=pages)
    required = set(item.hashedimage for item in informations)
    # TODO: EXTEND FILE EXT?
    files = utila.file_list(path, include=IMAGE_EXT)
    result = []
    for item in files:
        hashedimage = utila.file_name(item)
        if hashedimage not in required:
            # image is not required
            continue
        fileext = utila.file_ext(item)
        loaded = utila.file_read_binary(os.path.join(path, item))
        raw = RawImage(name=hashedimage, ext=fileext, raw=loaded)
        result.append(raw)
    return result


def image_filename(path, hashed) -> str:
    for ext in IMAGE_EXT:
        imagepath = os.path.join(path, f'{hashed}.{ext}')
        if not os.path.exists(imagepath):
            continue
        return os.path.split(imagepath)[1]
    return None


def zip_images(path: str, pages: tuple = None) -> ZippedImageInfos:
    informations = load_image_informations(path, pages=pages)
    result = [
        ZippedImageInfo(info, image_filename(path, info.hashedimage))
        for info in informations
    ]
    return result


def select_images(items, page):
    if not items:
        return []
    return [item for item in items if item[0].page == page]
