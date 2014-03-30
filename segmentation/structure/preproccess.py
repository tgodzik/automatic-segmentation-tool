from bs4 import BeautifulSoup
import re

def strip(html_doc):
    soup = BeautifulSoup(html_doc)
    # strip head
    body = soup.find("body")
    for i in body.find_all('script'):
        i.decompose()
    return body


def break_up(input):

    blocks = []

    def go_down(tag):
        children = [i for i in tag.children]
        if len(children) == 0:
            print tag
        else:
            for i in children:
                go_down(i)

    # mark segments and return list
    #for i in input.contents:
    #    print i
    #print input.contents
    go_down(input)
    return blocks


def prepare(page):
    stripped = strip(page)
    broken = break_up(stripped)
    return broken


doc = open("../../pages/page1.html").read()
prepare(doc)