from bs4 import BeautifulSoup
import re


def strip(html_doc):
    soup = BeautifulSoup(html_doc)
    # strip head
    body = soup.find("body")
    for i in body.find_all('script'):
        i.decompose()
    return body


# we need to find by having text and if the length of text does not equal sum of length of children texts then that is the largest possible node text
def break_up(input):
    blocks = []

    def go_down(tag):
        if hasattr(tag, 'children'):
            children = [j for j in tag.children]
            if len(children) == 1 and len(tag.text) > 0:
                blocks.append(tag)
            else:
                for i in tag.children:
                    if hasattr(i, 'text') and len(i.text) > 0:
                        go_down(i)

    go_down(input)
    return blocks


def prepare(page):
    stripped = strip(page)
    broken = break_up(stripped)
    return broken


doc = open("../../pages/page1.html").read()
for i in prepare(doc):
    print i
    print "-----------------------------------------------"