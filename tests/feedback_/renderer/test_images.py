# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import webbrowser

import utila

import feedback.renderer.images
import tests.resources
from tests.feedback_.fixtures import leftright  # pylint:disable=W0611


def test_renderer_title_with_image(tmpdir, leftright):  # pylint:disable=W0621
    outpath = os.path.join(tmpdir.strpath, 'title.html')
    titlepage = utila.select_page(leftright, 0)

    rendered = feedback.renderer.html.render_page(titlepage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    if utila.single_execution():
        webbrowser.open(outpath)


def test_load_image_informations():
    source = tests.resources.LEFTRIGHT_GENERATED
    informations = feedback.renderer.images.load_image_informations(source)
    assert len(informations) == 5, str(informations)


def test_load_image():
    source = tests.resources.LEFTRIGHT_GENERATED
    images = feedback.renderer.images.load_images(source)
    assert len(images) == 5
