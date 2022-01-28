# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import feedback.renderer.images


def test_renderer_title_with_image(tmpdir, leftright):  # pylint:disable=W0621
    outpath = os.path.join(tmpdir.strpath, 'title.html')
    titlepage = utila.select_page(leftright, 0)

    rendered = feedback.renderer.html.render_page(titlepage)
    assert len(rendered) > 300, str(rendered)

    utila.file_create(outpath, rendered)

    with utilatest.open_webbrowser(outpath):
        pass


@utilatest.requires(power.BOOK007_PDF)
def test_load_image_informations():
    source = power.link(power.BOOK007_PDF)
    source = os.path.join(source, 'rawmaker__images_images')
    informations = feedback.renderer.images.load_image_informations(source)
    # figures are merged into images
    assert len(informations) in (4, 8), str(informations)


@utilatest.requires(power.BOOK007_PDF)
def test_load_image():
    source = power.link(power.BOOK007_PDF)
    source = os.path.join(source, 'rawmaker__images_images')
    images = feedback.renderer.images.load_images(source)
    # figures are merged into images
    assert len(images) in (4, 8)
    exts = sorted([item.ext for item in images])
    expected = ['jpg', 'jpg', 'jpg', 'jpg']
    expected2 = ['png', 'png', 'png', 'png', 'png', 'png', 'png', 'png']
    assert exts in (expected, expected2)


def test_renderer_figures_as_image(tmpdir, master116):  # pylint:disable=W0621
    outpath = os.path.join(tmpdir.strpath, 'index.html')
    titlepage = utila.select_page(master116, 2)

    rendered = feedback.renderer.html.render_page(titlepage)
    assert len(rendered) > 300, str(rendered)

    with utilatest.open_webbrowser(outpath):
        utila.file_create(outpath, rendered)
