__author__ = 'Tomasz Godzik'

from BeautifulSoup import BeautifulSoup

#html_doc = open("html_data/katowice.html").read()

# raczej zrobmy by dalo sie dopisywac do beautiful soup - dodatkowe adnotacje


class HtmlNode:
    def __init__(self):
        self.children = []
        self.text = ""


def recursive_create(node):
    children = node.findChildren(recursive=False)

    base = HtmlNode()
    base.text = node.text

    # find text
    for c in children:
        print c.name
        base.children.append(recursive_create(c))

    return base


doc = open("html_data/segment1.html").read()
soup = BeautifulSoup(doc)

tree = recursive_create(soup)


def recursive_print(node):
    print node.text, "\n"

    for c in node.children:
        recursive_print(c)

recursive_print(tree)