__author__ = 'Tomasz Godzik'
# -*- coding: utf-8 -*-

import re
import segmentation.structure.preproccess as pre


class Segment:
    def __init__(self, tag):
        self.tags = [tag]
        self.simplify()
        self.density = self.calculate_density()

    def __add__(self, other):
        self.tags.extend(other.tags)
        self.calculate_density()
        return self

    def __sub__(self, other):
        return abs(self.density - other.density)

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
            return len(found) / lines
        else:
            found = re.findall(regexp, text, re.UNICODE)
            return len(found)


def segment(names, treshold=1.5):

    ret_list = []
    for name in names:
        html_doc = open(name).read()
        segs = pre.prepare(html_doc)
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