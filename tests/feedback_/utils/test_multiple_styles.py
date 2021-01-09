# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import feedback.utils.multiple_styles as fums


def test_merge():
    msg = 'Hier!Spricht Helm'
    first = fums.Style(0, 5, '<bat>', '</bat>')
    second = fums.Style(4, 10, '<cat>', '</cat>')

    styles = [first, second]
    result = fums.merger(msg, styles)
    expected = '<bat>Hier</bat><bat><cat>!</cat></bat><cat>Spric</cat>ht Helm'
    assert result == expected, str(result)


def test_merge_raw():
    msg = 'Hier Spricht Helm'
    raw = fums.create_raw(msg)
    merged = fums.tostring(msg, [raw])
    assert merged == msg, merged


def test_merge_two_styles():
    first = fums.Style(0, 5, '<bat>', '</bat>')
    second = fums.Style(4, 10, '<cat>', '</cat>')

    merged = fums.merge_two(first, second)
    # yapf:disable
    expected = [
        fums.Style(start=0, end=4, first='<bat>', last='</bat>'),
        fums.Style(start=4, end=5, first='<bat>{*}<cat>', last='</bat>{*}</cat>'),
        fums.Style(start=5, end=10, first='<cat>', last='</cat>'),
    ]
    # yapf:enable
    assert merged == expected


def test_merge_multiple_overlapping():
    text = '0123456789'
    styles = [
        fums.Style(start=0, end=10, first='<A>', last='</A>'),
        fums.Style(start=3, end=6, first='<B>', last='</B>'),
    ]
    exepected = '<A>012</A><A><B>345</B></A><A>6789</A>'
    result = fums.merger(text, styles)
    assert result == exepected, str(result)


def test_merge_multiple_overlapping_tripple():
    text = '01234567891012'
    styles = [
        fums.Style(start=0, end=10, first='<A>', last='</A>'),
        fums.Style(start=3, end=6, first='<B>', last='</B>'),
        fums.Style(start=8, end=10, first='<C>', last='</C>'),
    ]
    exepected = '<A>012</A><A><B>345</B></A><A>67</A><A><C>89</C></A>1012'
    result = fums.merger(text, styles)
    assert result == exepected, str(result)


@pytest.mark.xfail(reason='improve optimizer')
def test_optimize_merger():
    styles = [
        fums.Style(
            start=0,
            end=93,
            first='<span id="line3_16">',
            last='</span>',
        ),
        fums.Style(
            start=0,
            end=44,
            first='<span style="font-size:12.0px;font-family:TimesNewRoman;">',
            last='</span>',
        ),
        fums.Style(
            start=44,
            end=50,
            first=
            '<span style="font-size:12.0px;font-style:italic;font-family:TimesNewRoman;">',
            last='</span>',
        ),
        fums.Style(
            start=50,
            end=93,
            first='<span style="font-size:12.0px;font-family:TimesNewRoman;">',
            last='</span>',
        ),
    ]
    text = 'X' * 93
    result = fums.merger(text, styles)

    better = '<span id="line3_16"><span'\
        'style="font-size:12.0px;font-family:TimesNewRoman;">XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</span><span '\
        'style="font-size:12.0px;font-style:italic;font-family:TimesNewRoman;">XXXXXX</span><span '\
        'style="font-size:12.0px;font-family:TimesNewRoman;">XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</span></span>'
    assert result == better

    best = ('<span id="line3_16"><span style="font-family:TimesNewRoman;'
            'font-size:12px">XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            '<span style="italic;">XXXXXX</span>XXXXXXXXXXXXXXXXXXXXXXXX'
            'XXXXXXXXXXXXXXXXXXX</span></span>')
    assert result == best

    # TODO: ADD BEST TO OPTIMIZE FONT FAMILIY AND FONT SIZE
    # IDEA: USE A SPAN FIELD FOR EVERY STYLE TO IMPROVE OPTIMIZING POSSIBILITIES


def test_optimize_abb_regression():
    text = 'Abb. 2.2.: Topologie Paralleler Hybrid - 1 Batterie, 2 Kraftstofftank, 3 Getriebe, 4'
    styles = [
        fums.Style(
            start=0,
            end=181,
            first='<span id="line12_5">',
            last='</span>',
        ),
        fums.Style(
            start=0,
            end=11,
            first=
            '<span style="font-size:9.96px;font-family:Consolas;font-family:LMRoman10;">',
            last='</span>',
        ),
        fums.Style(
            start=11,
            end=85,
            first=
            '<span style="font-size:9.96px;font-family:Consolas;font-family:LMRoman10;">',
            last='</span>',
        )
    ]
    result = fums.merger(text, styles)
    expected = ('<span id="line12_5"><span style="font-size:9.96px;'
                'font-family:Consolas;font-family:LMRoman10;">Abb. 2.2.: '
                'Topologie Paralleler Hybrid - 1 Batterie, 2 Kraftstofftank,'
                ' 3 Getriebe, 4</span></span>')
    assert result == expected


def test_optimize_style_abb_regression():
    text = 'Abb. 2.1.: Topologie Serieller Hybrid - 1 Elektrischer Fahrmotor, 2 Kraftstofftank, 3 Leistungs­-'
    styles = [
        fums.Style(
            start=0,
            end=11,
            first='<span id="line12_4">',
            last='</span>',
        ),
        fums.Style(
            start=0,
            end=11,
            first='<span style="font-size:9.96px;font-family:LMRoman10;">',
            last='</span>',
        ),
        fums.Style(
            start=11,
            end=96,
            first='<span style="font-size:9.96px;font-family:LMRoman10;">',
            last='</span>',
        ),
    ]
    result = fums.merger(text, styles)
    # TODO: NOT PERFECT, BUT WORKS AT THE MOMENT. PLEASE REPLEASE IF NECESSARY
    expected = (
        '<span style="font-size:9.96px;font-family:LMRoman10;"><span id="line12_4">'
        'Abb. 2.1.: </span></span><span style="font-size:9.96px;font-family:LMRoman10;">'
        'Topologie Serieller Hybrid - 1 Elektrischer Fahrmotor, 2 Kraftstofftank, '
        '3 Leistungs­</span>-')
    assert result == expected


@pytest.mark.xfail(reason='regression test which is not solved')
def test_regression_merge_style():
    text = 'of language which is independent in meaning and form.“65'
    # yapf:disable
    style = [
        fums.Style(start=46, end=80, first='<span id="line35_5">', last='</span>'),
        fums.Style(start=0, end=2, first='<span id="word35_49">', last='</span>'),
        fums.Style(start=3, end=11, first='<span id="word35_50">', last='</span>'),
        fums.Style(start=12, end=17, first='<span id="word35_51">', last='</span>'),
        fums.Style(start=18, end=20, first='<span id="word35_52">', last='</span>'),
        fums.Style(start=21, end=32, first='<span id="word35_53">', last='</span>'),
        fums.Style(start=33, end=35, first='<span id="word35_54">', last='</span>'),
        fums.Style(start=36, end=43, first='<span id="word35_55">', last='</span>'),
        fums.Style(start=44, end=47, first='<span id="word35_56">', last='</span>'),
        fums.Style(start=48, end=56, first='<span id="word35_57">', last='</span>'),
        fums.Style(start=0, end=52, first='<span style="font-size:12.0px;font-family:Times;font-style:italic;">', last='</span>'),
        fums.Style(start=52, end=54, first='<span style="font-size:12.0px;font-family:Times-Roman;">', last='</span>'),
        fums.Style(start=54, end=56, first='<span style="font-size:8.04px;font-family:Times-Roman;"><sup>', last='</sup></span>'),
    ]
    # yapf:enable
    merged = fums.merger(text, style)
