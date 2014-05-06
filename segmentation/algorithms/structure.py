import re
import json

from bs4 import BeautifulSoup

from segmentation.metrics.measurement import measure
from segmentation.metrics.visual_blocks import visualize


def strip(html_doc):
    """Removes unnecessary tags

    """
    doc = re.sub("[\s]+", " ", html_doc)
    soup = BeautifulSoup(doc)
    stripped = ["script", "noscript", "link", "iframe", "meta"]

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


def algorithm(segment):
    def main(files, is_measured=False, measure_files=None, visualized=False, verbose=True, treshold=None):
        """  Main algorithmfor measurement purposes.
        :param files list of tuples for measuring the performance of simple list of names

        """
        if not measure_files:
            measure_files = []

        #open all needed files
        pages = [open(f).read() for f in files]

        if verbose:
            print "Analyzing files " + ",".join(files)

        #use segmentation
        checked = segment(pages, treshold)

        #measure
        if is_measured:
            # open refrence pages
            ref = [json.load(open(f)) for f in measure_files]

            to_check = [map(lambda x: str(x).decode('utf-8'), i) for i in checked]

            if verbose:
                print "Measuring performance"

            for i in range(0, len(ref)):
                results = measure([0, 1], ref[i], to_check[i])
                if verbose:
                    print str(files[i]) + " - " + str(results)

        #visualize
        if visualized:
            for i in range(0, len(checked)):
                visualize(checked[i], "result{index}.html".format(index=i))

        return checked

    return main
