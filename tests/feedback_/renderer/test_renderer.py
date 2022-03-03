# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import protocol
import pytest
import utila
import utilatest

import feedback.features.view as ffpv
import feedback.renderer.html
import feedback.renderer.loader
import feedback.renderer.mark
import tests.feedback_.renderer as tfr


def test_renderer_load(masterpage72):
    assert masterpage72


@pytest.mark.xfail(reason='duplicated horizontal line rendering')
def test_renderer_firstpage(tmpdir, masterpage72):
    with tfr.render_and_open(tmpdir, masterpage72, 0) as html:
        assert '<hr' not in html, html


def test_renderer_secondpage_mark_line_and_words(tmpdir, masterpage72):
    # TODO: VERIFY WITH SELENIUM
    outpath = os.path.join(tmpdir, 'secondpage.html')
    secondpage = utila.select_page(masterpage72, 1)

    marks = feedback.renderer.mark.PageMarkConfiguration(
        page=1,
        wordmarks=set([1, 2, 3, 4, 5]),
        linemarks=set([4, 5, 20]),
    )

    rendered = feedback.renderer.html.render_page(secondpage, marks=marks)
    assert len(rendered) > 300, str(rendered)

    style = """\
        <style>
        #line1_20{
            background:red;
        }
        </style>
        """
    output = style + rendered
    with utilatest.open_webbrowser(outpath):
        utila.file_create(outpath, output)


def test_renderer_shapes_mark_bounding(tmpdir, leftright):
    """Render first page of `leftright` example and add a red rectangle
    in the top center of the page."""
    shapes = [
        {
            'type': 'rectangle',
            'bounding': (50, 50, 400, 400),
            'border': '1px solid red',
        },
    ]
    with tfr.render_and_open(tmpdir, leftright, page=0, shapes=shapes) as html:
        assert '1px solid red' in html  # ensure to render red box


@utila.todo(major=3, minor=2, description='verify with selenium')
def test_renderer_toc(tmpdir, masterpage72):
    """This test aims to generate and view a toc very fast to check
    develop new html renderings."""
    with tfr.render_and_open(tmpdir, masterpage72, page=1):
        # check that page number are on vertical line
        pass


def test_render_page_with_horizontals(tmpdir, masterpage72):
    """Render footnote separator."""
    with tfr.render_and_open(tmpdir, masterpage72, page=3) as html:
        assert '<hr' in html, str(html)


def test_render_bachelor56_title_page(tmpdir, bachelor56):
    with tfr.render_and_open(tmpdir, bachelor56, page=0) as html:
        # ensure to render university logo
        assert '<img src=' in html, html


def test_render_bachelor56_italic_style(tmpdir, bachelor56):
    with tfr.render_and_open(tmpdir, bachelor56, page=5) as html:
        assert 'font-style:italic;' in html, str(html)


def test_render_bachelor56_render_table(tmpdir, bachelor56):
    with tfr.render_and_open(tmpdir, bachelor56, page=15) as html:
        # ensure that table lines are rendered
        assert html.count('<svg  style') > 20, html


def test_render_bachelor56_page20(tmpdir, bachelor56):
    page = 10
    wordmarks = {15, 16, 17, 18, 19, 20, 21, 22}
    mark = feedback.renderer.mark.PageMarkConfiguration(
        page=page,
        wordmarks=wordmarks,
    )
    with tfr.render_and_open(tmpdir, bachelor56, marks=mark, page=page) as html:
        assert html.count('id="word10_') == len(wordmarks)


def test_sentence_selector(bachelor56):
    content = bachelor56
    selected = utila.select_page(content, 10)
    matched = (
        'Dieser Effekt wird umso effektiver, umso häufiger Alkohol '
        'konsumiert wird. Voraussetzung, um solche Reaktionen zu zeigen, sind '
        'jedoch verlässliche Hinweisreize und die Erfahrung von positiven '
        'Konsequenzen, wenn die Beeinträchtigung durch den Alkohol '
        'kompensiert werden können.')
    generator = feedback.renderer.mark.WordGenerator()
    left = []
    for line in selected.navigator:
        left.extend([item[1] for item in generator.words(line.text)])
    generator = feedback.renderer.mark.WordGenerator()
    right = [item for _, item in generator.words(matched)]
    items = feedback.renderer.mark.best_sync(left, right)
    assert len(items) > 20


@utilatest.requires(power.BACHELOR056_PDF)
def test_render_bachelor56_page9_with_quotation_error():
    """Ensure to load sentences marks."""
    source = power.link(power.BACHELOR056_PDF)
    sentences, wordx = {}, {}
    # load findings
    findings = protocol.findings_from_path(source)
    # NOT VALIDATED but data/algo had changed if broken
    assert len(findings) in (20, 19)
    marks = ffpv.load_marks(findings, sentences, wordx)
    assert marks
    # TODO: GIVE THIS TEST A PURPOSE


def test_render_master72_marked_lines(tmpdir, masterpage72):
    """This test aims to generate and view a toc very fast to check
    develop new html renderings."""
    pagemarks = feedback.renderer.mark.PageMarkConfiguration(
        page=3,
        wordmarks=[],
        linemarks=[0, 16, 19],
    )

    css = """\
        #line3_19, #line3_16, #line3_0{
            background:red;
        }
    """
    with tfr.render_and_open(
            tmpdir,
            masterpage72,
            page=3,
            marks=pagemarks,
            css=css,
    ) as source:
        # three lines are marked
        assert source.count('id="line3_0"') == 1
        assert source.count('id="line3_16"') >= 1
        assert source.count('id="line3_19"') >= 1


@utilatest.requires(power.MASTER116_PDF)
def test_regression_render_master116_marked_lines_page12(tmpdir, master116):
    page = 12
    pagemarks = feedback.renderer.mark.PageMarkConfiguration(
        page=page,
        wordmarks=[],
        linemarks=[4, 5],
    )
    expected = 4
    css = """\
        #line12_4{
            background:blue;
        }
        #line12_5{
            background:red;
        }
    """
    with tfr.render_and_open(
            tmpdir,
            master116,
            page=page,
            marks=pagemarks,
            css=css,
    ) as source:
        # regression test after improving merger
        assert source.count('Abb. 2.1.: ') == 1
        assert source.count('Abb. 2.2.: ') == 1
        assert source.count(f'id="line{page}_{expected}"') == 1


@utilatest.requires(power.DISS264_PDF)
def test_regression_render_diss264_page21(testdir):
    path = power.link(power.DISS264_PDF)
    loaded = feedback.renderer.loader.from_path(path)

    page = 21
    with tfr.render_and_open(testdir.tmpdir, loaded, page=page) as source:
        # character in figure are removed by rawmaker_cleanup
        assert not source.count('transform:')  # adjust later


@utilatest.requires(power.BACHELOR090_PDF)
def test_figure_notext(testdir):
    """Do not render text in figure area twice."""
    path = power.link(power.BACHELOR090_PDF)
    page = 23
    loaded = feedback.renderer.loader.from_path(path, pages=page)
    with tfr.render_and_open(testdir.tmpdir, loaded, page=page) as source:
        # figure content
        assert 'RTR' not in source
