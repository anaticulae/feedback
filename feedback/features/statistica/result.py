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

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import Template
from utila import NEWLINE
from utila import file_create
from utila import file_read
from utila import from_raw_or_path
from yaml import load_all as from_yaml
from yaml.loader import SafeLoader

from feedback import ROOT

TEMPLATES = join(ROOT, 'feedback/features/statistica/templates')
assert exists(TEMPLATES), TEMPLATES

TEMPLATE_CHAPTER = join(TEMPLATES, 'chapter.html')
assert exists(TEMPLATE_CHAPTER), TEMPLATE_CHAPTER


def generate(source, sink: str):
    # DIRTY HACK THIS IS SO DIRTY!
    alpha_content = list(load(source[0]))
    words = list(load(source[2]))[0]
    chapter = alpha_content[1]
    loaded = list(load(source[1]))[0]

    chapter = {item['title']: item['content'] for item in chapter}

    with_content = []
    for line in loaded:
        text = chapter[line['title']]

        tags = line['sentence_shortest'][0:3] + line['sentence_longest'][0:5]
        print(tags)
        tagged = tag_content(text, tags)
        line['text'] = tagged

        with_content.append(line)

    result = render(with_content, words)

    # TODO: Add override flag
    file_create(sink, result)


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

    chapters = from_yaml(content, Loader=SafeLoader)
    return chapters


def strip_jinja(content: str):
    """Remove whitespace from comments of jinja template

    Remove lines with whitespaces
    """
    clean = [
        item.rstrip() for item in content.splitlines() if item and item.strip()
    ]
    return NEWLINE.join(clean)


def render(chapters: list, words: list):
    loader = PackageLoader('feedback.features.statistica')
    content = loader.get_source(None, 'chapter.html')[0]
    # content = file_read(TEMPLATE_CHAPTER)
    chapter = Template(content)
    result = chapter.render(encoding='utf8', chapters=chapters, words=words)
    result = strip_jinja(result)
    return result
    # file_create(join(TEMPLATES, 'result.html'), result)
    # assert 0


#         >>> template.render(name='John Doe') == u'Hello John Doe!'
# '
# print(loader['a'])
# assert 0
# pass
