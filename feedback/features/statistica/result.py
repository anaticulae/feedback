# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os.path import exists
from os.path import join

from jinja2 import PackageLoader
from jinja2 import Template
from utila import NEWLINE
from utila import from_raw_or_path
from yaml import load_all as from_yaml
from yaml.loader import SafeLoader

from feedback import ROOT

TEMPLATES = join(ROOT, 'feedback/features/statistica/templates')
assert exists(TEMPLATES), TEMPLATES

# TODO: Replace template
TEMPLATE_CHAPTER = join(TEMPLATES, 'chapter.html')
assert exists(TEMPLATE_CHAPTER), TEMPLATE_CHAPTER

TEMPLATE_WORD = join(TEMPLATES, 'words.html')
assert exists(TEMPLATE_WORD), TEMPLATE_WORD


def generate(
        toc_and_chapter: str,
        texts: str,
        words: str,
):
    """
    Args:
        toc_and_chapter(str): path to generated file by rawmaker wich contains
                              the table of content of an document and the
                              content below.
        words(str): path to file wich which contains a list which contains a
                    descending list with [words, occurence]
        texts(str): path to file which contain some statistics, with longest
                    sentence, words of an chapter
    Returns:
        tuple(chapter, word): of generated content
    """
    chapter = load_chapters(toc_and_chapter)

    words = load_words(words)
    texts = load_text_statistics(texts)

    tagged = tagged_content(texts, chapter)
    word, chapter = render(tagged, words)

    return chapter, word


def render(chapters: list, words: list):
    loader = PackageLoader('feedback.features.statistica')
    chapter_template = Template(loader.get_source(None, 'chapter.html')[0])
    word_template = Template(loader.get_source(None, 'words.html')[0])

    chapter = chapter_template.render(chapters=chapters)
    word = word_template.render(words=words)
    return chapter, word


def load_chapters(path: str):
    """Raw maker result"""
    loaded = load(path)[1]  # we need the second file

    # link chapter content to title
    chapter = {item['title']: item['content'] for item in loaded}
    return chapter


def load_words(path: str) -> list:
    """Return descending list with a pair of word and occurence"""
    words = load(path)[0]  # use first file
    assert isinstance(words, list)
    converted = [(item[0], item[1]) for item in words]
    return converted


def load_text_statistics(path: str):
    return load(path)[0]


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
    raw = list(raw)  # load complete generator
    return raw


def strip_jinja(content: str):
    """Remove whitespace from comments of jinja template

    Remove lines with whitespaces
    """
    clean = [
        item.rstrip() for item in content.splitlines() if item and item.strip()
    ]
    return NEWLINE.join(clean)
