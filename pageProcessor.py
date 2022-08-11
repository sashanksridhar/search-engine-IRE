import textProcessor
import regexExp
import re

def process(data):
    data = data.lower()
    data = regexExp.reUrl.sub('', data)
    data = regexExp.reTags.sub('', data)
    data = regexExp.reCite.sub('', data)
    data = regexExp.reFile.sub('', data)
    tokens = textProcessor.tokenize(data)
    return textProcessor.stem_and_stop(tokens), len(tokens)


def process_category(data):
    data = data.split('\n')
    categories = []
    for line in data:
        if re.match(r'\[\[category', line):
            categories.append(re.sub(r'\[\[category:(.*)\]\]', r'\1', line))
    return process(' '.join(categories))

def process_infobox(data):
    data = data.split('\n')
    flag = 0
    info = []
    for line in data:
        if re.match(r'\{\{infobox', line):
            flag = 1
            info.append(re.sub(r'\{\{infobox(.*)', r'\1', line))
        elif flag == 1:
            if line == '}}':
                flag = 0
                continue
            info.append(line)
    return process(' '.join(info))

def process_links(data):
    data = data.split('\n')
    links = []
    # for line in data:
    #     if re.match(r'\*[\ ]*\[', line):
    #         links.append(line)
    flag = 0
    for line in data:
        if re.match(r'==external links==', line):
            flag = 1
        elif flag == 1:
            if line == ' }}':
                break
            if 'http' in line:
                links.append(line)

    return process(' '.join(links))


def process_references(data):

    data = data.split('\n')
    refs = []
    for line in data:
        if re.search(r'<ref', line):
            refs.append(re.sub(r'.*title[\ ]*=[\ ]*([^\|]*).*', r'\1', line))

    return process(' '.join(refs))


def process_body(data):
    return process(data)

