# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import detector.feature.titlepage
import utila

import feedback
import tests.resources


def install_requirements():
    utila.clean_install(feedback.ROOT, feedback.PACKAGE)


def sync_resources():
    completed = utila.run('power --all', tests.resources.RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)


def extract_examples():
    todo = create_todo_rawmaker(
        'restruct/restructuredtext.pdf',
        './restruct',
    )\
    + create_todo_sections('./restruct')\
    + create_todo_groupme('./restruct')\
    + create_todo_words('./restruct')

    for (executable, inpath, outpath, configuration) in todo:
        cmd = f'{executable} -i {inpath} -o {outpath} {configuration}'
        utila.debug(f'run {cmd}')
        completed = utila.run(cmd, cwd=tests.resources.RESOURCES)
        assert completed.returncode == utila.SUCCESS, str(completed)
        utila.debug('completed')


def create_todo_rawmaker(inpath, outpath):
    result = [
        (
            'rawmaker',
            inpath,
            outpath,
            detector.feature.titlepage.RAWMAKER_CONFIGURATION,
        ),
        (
            'rawmaker',
            inpath,
            outpath,
            ('--border --boxes --font --text --toc '
             '--char_margin=5.0 --boxes_flow=1.0 --line_margin=0.3'),
        ),
    ]
    return result


def create_todo(process, path, todo):
    result = [
        (process, path, path, todo),
    ]
    return result


def create_todo_sections(path):
    return create_todo(
        'sections',
        path,
        '--chapter --index --sections --title --toc --whitepage',
    )


def create_todo_groupme(path):
    return create_todo(
        'groupme',
        path,
        '--footer --pagenumbers',
    )


def create_todo_words(path):
    return create_todo(
        'words',
        path,
        '--headlines --boxed --list --text --words',
    )
