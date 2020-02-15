#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
UTF8 = 'utf8'

with open(os.path.join(ROOT, 'README.md'), mode='rt', encoding=UTF8) as fp:
    README = fp.read()

VERSION_PATH = os.path.join(ROOT, 'feedback/__init__.py')
with open(VERSION_PATH, mode='rt', encoding=UTF8) as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

REQUIREMENTS_PATH = os.path.join(ROOT, 'requirements.txt')
with open(REQUIREMENTS_PATH, mode='rt', encoding=UTF8) as fp:
    INSTALL_REQUIRES = [
        line for line in fp.readlines() if line and '#' not in line
    ]


def datafiles():
    return [
        ('.', [
            'CHANGELOG.md',
            'README.md',
            'requirements.txt',
        ]),
        ('feedback/templates/statistica', [
            'feedback/templates/statistica/chapter.html',
            'feedback/templates/statistica/words.html',
        ]),
        ('feedback/templates/fonts', [
            'feedback/templates/fonts/fonts_used.html',
            'feedback/templates/fonts/fonts_ugly_badfont.html',
        ]),
        ('feedback/templates/problems', [
            'feedback/templates/problems/index.html',
        ]),
    ]


if __name__ == "__main__":
    # allow setup.py to run from another directory
    os.chdir(ROOT)
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        data_files=datafiles(),
        description='It\'s important!',
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        long_description=README,
        name='feedback',
        platforms='any',
        url='https://dev.package.checkitweg.de/feedback',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'feedback',
            'feedback.command',
            'feedback.command.decider',
            'feedback.features',
            'feedback.features.fonts',
            'feedback.features.problems',
            'feedback.features.statistica',
            'feedback.problems',
            'feedback.renderer',
            'feedback.templates',
        ],
        entry_points={
            'console_scripts': [
                'feedback = feedback.cli:main',
                'feedback_decider_fonts = feedback.command.decider.fonts:main',
                'feedback_statistica = feedback.command.statistica:main',
            ],
        },
    )
