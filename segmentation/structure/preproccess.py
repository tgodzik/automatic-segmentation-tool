from bs4 import BeautifulSoup
import re


def strip(html_doc):
    doc = re.sub("[\s]+", " ", html_doc)
    soup = BeautifulSoup(doc)
    stripped = ["script", "noscript", "link", "iframe"]

    # strip head
    body = soup.find("body")
    for s in body.find_all(stripped):
        s.decompose()
    return body


def break_up(page):

    # tags that could be segments
    segment_tags = {"div", "head", "table", "center", "body", "section", "p", "span", "ul", "li"}

    def search(tag):
        if hasattr(tag, 'children'):
            children = {c.name for c in tag.children}
            if len(segment_tags & children) == 0:
                return [tag]
            else:
                ret_list = []
                for c in tag.children:
                    if c.name in segment_tags:
                        ret_list.extend(search(c))
                return ret_list

    return search(page)


def prepare(page):
    stripped = strip(page)
    broken = break_up(stripped)
    return broken


