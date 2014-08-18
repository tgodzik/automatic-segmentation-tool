__author__ = 'Tomasz Godzik'
# -*- coding: utf-8 -*-

from .segment import Segment


def simplify(seg):
    parent = seg.tags[0].parent

    if len(seg.tags) == len(parent.find_all()):
        seg.tags = [parent]
        simplify(seg)


def break_up(tag):
    if hasattr(tag, 'children'):
        children = {c.name for c in tag.children}
        children = set(filter(lambda x: x, children))
        if len(children) == 0 or len(children.intersection({"a", "strong", "br"})) is not 0:
            return [Segment(tag)]
        else:
            ret_list = []
            for c in tag.children:
                if c.name is not None:
                    ret_list.extend(break_up(c))
            return ret_list


def block_fusion(segments, treshold=0.5):
    """ Function responsible for segmentation
    :param segments segments to be divided
    :param treshold join threshold
    :returns lists of divided segments

    """

    divided = []

    for segment in segments:

        tmp = [break_up(i) for i in segment.tags]
        blocks = []
        map(blocks.extend, tmp)

        change = True

        while change:
            change = False
            new_blocks = []
            for i in range(0, len(blocks) - 1):
                if blocks[i] and blocks[i].difference(blocks[i + 1]) < treshold:
                    new = blocks[i] + blocks[i + 1]
                    simplify(new)
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

        divided.append(blocks)

    return divided


