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

import glob
import os
import typing

# TODO: REPLACE WITH UTILA CODE
import rawmaker.images.info
import utila

ImageInformations = typing.List[rawmaker.images.info.ImageInformation]


def load_image_informations(path: str) -> ImageInformations:
    result = []
    path = os.path.join(path, 'rawmaker__images_images')
    # TODO: REMOVE WITH UTILA CODE
    with utila.chdir(path):
        files = glob.glob('*.yaml')
        for item in files:
            source = os.path.join(path, item)
            loaded = rawmaker.images.info.load_info(source)
            result.append(loaded)
    return result


def load_images(path: str) -> list:
    result = []
    path = os.path.join(path, 'rawmaker__images_images')
    # TODO: REMOVE WITH UTILA CODE
    with utila.chdir(path):
        files = os.scandir(path)
        # TODO: REMOVE WITH UTILA SORT METHOD
        for item in sorted(files, key=lambda x: int(x.name.split('.')[0])):
            if item.name.endswith('.yaml'):
                continue
            source = os.path.join(path, item)
            loaded = utila.file_read_binary(source)
            result.append((item.name, loaded))
    return result
