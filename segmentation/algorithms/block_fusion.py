__author__ = 'Tomasz Godzik'
# -*- coding: utf-8 -*-

from segmentation.algorithms.structure import prepare, algorithm
from .segment import DensitySegment


def block_fusion(html_docs, treshold=0.5):
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
            blocks.append(DensitySegment(i))

        change = True

        while change:
            change = False
            new_blocks = []
            for i in range(0, len(blocks) - 1):
                if blocks[i] and blocks[i] - blocks[i + 1] < treshold:
                    new = blocks[i] + blocks[i + 1]
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


block_fusion_algorithm = algorithm(block_fusion)

