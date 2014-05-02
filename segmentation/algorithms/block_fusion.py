__author__ = 'Tomasz Godzik'
# -*- coding: utf-8 -*-

import re
from segmentation.structure.preproccess import prepare
from segmentation.metrics.measurement import measure
from segmentation.visualize.visual_blocks import visualize
import json
import logging


class Segment:
    """Class representing a single segment.
    """

    def __init__(self, tag):
        self.tags = [tag]
        self.simplify()
        self.density = self.calculate_density()

    def __add__(self, other):
        self.tags.extend(other.tags)
        self.density = self.calculate_density()
        return self

    def __sub__(self, other):
        if self.density == 0.0 or other.density == 0.0:
            return 0.0
        return abs(self.density - other.density) / max(self.density, other.density)

    def simplify(self):
        parent = self.tags[0].parent

        if len(self.tags) == len(parent.find_all()):
            self.tags = [parent]
            self.simplify()

    def __str__(self):
        return "".join([str(i) for i in self.tags])

    def calculate_density(self, max_line=80):
        text = "".join([i.text for i in self.tags])
        regexp = "[a-zA-Z0-9ąęółśżźćńĘĄŁÓŚŻŹĆŃ]+"
        sum_len = len(text)
        lines = int(sum_len / max_line)
        if lines > 0:
            r = max_line * lines
            reduced_text = text[0:r]
            found = re.findall(regexp, reduced_text, re.UNICODE)
            return float(len(found)) / float(lines)
        else:
            found = re.findall(regexp, text, re.UNICODE)
            return float(len(found))


def segment(html_docs, treshold):
    """ Function responsible for segmentation
    :param html_docs list of html docs to be segmented
    :param treshold join threshold
    :returns list of pages' segments

    """

    ret_list = []

    for html_doc in html_docs:
        segs = prepare(html_doc)
        blocks = []

        for i in segs:
            blocks.append(Segment(i))

        change = True

        while change:
            change = False
            new_blocks = []
            for i in range(0, len(blocks) - 1):
                if blocks[i] and blocks[i] - blocks[i+1] < treshold:
                    new = blocks[i] + blocks[i+1]
                    new.simplify()
                    new_blocks.append(new)
                    change = True
                    blocks[i] = None
                    blocks[i + 1] = None
                elif blocks[i]:
                    new_blocks.append(blocks[i])
            if change:
                if blocks[-1]:
                    new_blocks.append(blocks[-1])
                blocks = new_blocks

        ret_list.append(blocks)

    return ret_list


def algorithm(files, is_measured=False, visualized=False, verbose=True, treshold=0.5):
    """  Main algorithm
    :param files list of tuples for measuring the performance of simple list of names

    """

    #open all needed files
    pages = [open(f[0]).read() for f in files] if is_measured else [open(f).read() for f in files]

    if verbose:
        logging.info("Analyzing files " + ",".join(files))

    #use segmentation
    checked = segment(pages, treshold)

    #measure
    if is_measured:
        # open refrence pages
        ref = [json.load(open(f[1])) for f in files]

        to_check = [map(lambda x: str(x).decode('utf-8'), i) for i in checked]

        if verbose:
            logging.info("Measuring performance")

        for i in range(0, len(ref)):
            results = measure([0, 1], ref[i], to_check[i])
            if verbose:
                logging.info(str(files[i]) + " - " + str(results))

    #visualize
    if visualized:
        visualize(checked[0])

    return checked