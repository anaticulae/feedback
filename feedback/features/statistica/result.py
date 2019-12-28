# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import Tuple

from utila import NEWLINE
from utila import Flag
from utila import from_raw_or_path
from yaml import load as from_yaml
from yaml.loader import SafeLoader

import feedback.templates


def work(
        rawtexts: str,
        words: str,
        text_statistic: str,
) -> Tuple[str, str]:
    """
    Args:
        text(str): path to generated file by rawmaker wich contains
                   the content of an document
        words(str): path to file wich which contains a list which contains a
                    descending list with [words, occurence]
        chapter(str): path to file which contain some statistics, with longest
                      sentence, words of an chapter
    Returns:
        tuple(chapter, word): of generated html content
    """
    chapters = load_chapters(rawtexts)
    words = load_words(words)
    texts = load_text_statistics(text_statistic)

    tagged = tagged_content(texts, chapters)

    chapter, word = render(tagged, words)
    return chapter, word


def render(chapters: list, words: list):
    chapter_template = feedback.templates.template('statistica', 'chapter.html')
    word_template = feedback.templates.template('statistica', 'words.html')

    chapter = chapter_template.render(chapters=chapters)
    word = word_template.render(words=words)
    return chapter, word


def load_chapters(path: str):
    """Raw maker result"""
    loaded = load(path)
    # link chapter content to title
    chapter = {item['title']: item['content'] for item in loaded}
    return chapter


def load_words(path: str) -> list:
    """Return descending list with a pair of word and occurence"""
    words = load(path)  # use first file
    assert isinstance(words, list)
    converted = [(item[0], item[1]) for item in words]
    return converted


def load_text_statistics(path: str):
    return load(path)


def tagged_content(loaded, chapter: dict):
    with_content = []
    for line in loaded:
        text = chapter[line['title']]

        tags = line['sentence_shortest'][0:3] + line['sentence_longest'][0:5]
        tagged = tag_content(text, tags)
        line['text'] = tagged

        with_content.append(line)
    return with_content


def tag_content(content, tags):
    content = content.replace(NEWLINE, ' ')
    for item in tags:
        cleaned = item[0:30].replace(' ', '')
        replaced = '<link id ="%s"><u>%s</u></link>' % (cleaned, item)

        if replaced in content:
            # Do not tag twice
            continue

        content = content.replace(item, replaced)
    return content


def load(content: str):
    content = from_raw_or_path(content)
    raw = from_yaml(content, Loader=SafeLoader)
    return raw


def strip_jinja(content: str):
    """Remove whitespace from comments of jinja template

    Remove lines with whitespaces
    """
    clean = [
        item.rstrip() for item in content.splitlines() if item and item.strip()
    ]
    return NEWLINE.join(clean)


def name():
    return 'feedback_statistica'


def commandline():
    return Flag(longcut=name(), message='export the html result of %s' % name())
