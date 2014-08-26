import re
from bs4 import BeautifulSoup, element
from pygraphviz import *


def prep(html_doc):
    """Removes unnecessary tags

    """
    doc = re.sub("[\s]+", " ", html_doc)
    soup = BeautifulSoup(doc)

    stripped = ["script", "noscript", "link", "iframe", "meta", "style"]

    # strip head
    body = soup.find("body")
    for s in body.find_all(stripped):
        s.decompose()

    comments = soup.findAll(text=lambda text: isinstance(text, element.Comment))
    [comment.extract() for comment in comments]

    empty_tags = [""]

    while len(empty_tags) > 0:
        empty_tags = soup.findAll(lambda tag: not tag.contents and (tag.string is None or not tag.string.strip()))
        [empty_tag.extract() for empty_tag in empty_tags]

    return body


import collections

names = collections.defaultdict(int)


def search(root):
    if hasattr(root, "children"):
        chs = filter(lambda x: isinstance(x, element.Tag), root.children)

        dc = {}
        for i in chs:
            dc[i.name + str(names[i.name])] = search(i)
            names[i.name] += 1

        if len(dc) == 0:
            return None
        else:
            return dc


def setit(dc, G, last):
    for key, value in dc.iteritems():
        G.add_node(key)
        G.add_edge(last, key)
        if value is not None:
            setit(value, G, key)


def writeit(dc, ll, level=0):
    for key, value in dc.iteritems():
        ll[level] += " " + ''.join([i for i in key if not i.isdigit()])

        if value is not None:
            writeit(value, ll, level + 1)


# specify pages to test
base = "/home/tomasz/Documents/master_thesis/test_data/"

# fileset = check_files(base)

file = "a.northfish.pl.html"

page = open(base + file).read()

ready = prep(page)

dc = search(ready)

# lines = collections.defaultdict(str)
# writeit(dc, lines)
#
# for k,l in lines.iteritems():
#     print l

G = AGraph()
G.add_node("body")
setit(dc, G, "body")

G.layout(prog='dot')

G.draw(file + '.png')