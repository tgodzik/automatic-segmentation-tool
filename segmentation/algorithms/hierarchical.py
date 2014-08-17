__author__ = 'Tomasz Godzik'

import numpy as np

from bs4 import element

from segmentation.algorithms.functions import prep, algorithm
from .segment import Segment
from .functions import cosine_similarity


def simple_cost(a, b, gap_score=1):
    """Simple cost of aligments
    :params a first number as string
    :params b second number as string
    :return cost as int

    """
    if a is None:
        return gap_score * int(b)
    elif b is None:
        return gap_score * int(a)
    else:
        return abs(int(a) - int(b))


def sequence_sim(a, b, cost=simple_cost):
    """Calculates similarity between 2 node sequences.
    :param a first number as string
    :param b second number as string
    :param cost cost function taking 2 parameters
    :return a tuple (numpy array of results, minimal cost)

    """

    lena = len(a)
    lenb = len(b)

    arr = np.zeros((lena + 1, lenb + 1), dtype=np.int)

    arr[0, 0] = 0

    for i in range(1, lena + 1):
        arr[i, 0] = arr[i - 1, 0] + cost(a[i - 1], None)

    for j in range(1, lenb + 1):
        arr[0, j] = arr[0, j - 1] + cost(None, b[j - 1])

    for i in range(1, lena + 1):
        for j in range(1, lenb + 1):
            match = arr[i - 1, j - 1] + cost(a[i - 1], b[j - 1])
            gapa = arr[i - 1, j] + cost(a[i - 1], None)
            gapb = arr[i, j - 1] + cost(None, b[j - 1])
            arr[i, j] = min(match, gapa, gapb)

    return arr, 1 - arr[lena, lenb] / (sum(map(float, a)) + sum(map(float, b)))


def aligment(a, b, arr, cost=simple_cost):
    """Calculates the string aligment of 2 node sequences.
    :param a first number as string
    :param b second number as string
    :param cost cost function taking 2 parameters
    :return tuple of aligments

    """

    i = len(a)
    j = len(b)

    a_aln = []
    b_aln = []

    while i > 0 and j > 0:
        if (arr[i, j] - cost(a[i - 1], b[j - 1])) == arr[i - 1, j - 1]:
            a_aln.insert(0, a[i - 1])
            b_aln.insert(0, b[j - 1])
            i -= 1
            j -= 1
        elif (arr[i, j] - cost(a[i - 1], None)) == arr[i - 1, j]:
            a_aln.insert(0, a[i - 1])
            b_aln.insert(0, 0)
            i -= 1
        elif (arr[i, j] - cost(None, b[j - 1])) == arr[i, j - 1]:
            a_aln.insert(0, 0)
            b_aln.insert(0, b[j - 1])
            j -= 1
        else:
            print "error"

    while i > 0:
        a_aln.insert(0, a[i - 1])
        b_aln.insert(0, 0)
        i -= 1

    while j > 0:
        a_aln.insert(0, 0)
        b_aln.insert(0, b[j - 1])
        j -= 1

    return a_aln, b_aln


def multi_sequence_sim(a, b, cost=simple_cost):
    sum_sim = 0.0
    for i in range(0, min(len(a), len(b))):
        _, res = sequence_sim(a[i], b[i])
        sum_sim += res
    return sum_sim / len(a)


def search(root, acc, level=0):
    if hasattr(root, "children"):
        chs = filter(lambda x: isinstance(x, element.Tag), [i for i in root.children])
        count = len(chs) + 1
        if len(acc) <= level:
            acc.append([])
        acc[level].append(count)
        for i in chs:
            search(i, acc, level + 1)
        return acc


def dual_search(root1, root2, acc1, acc2, treshold):
    if hasattr(root1, "children") and hasattr(root2, "children"):
        chs1 = filter(lambda x: isinstance(x, element.Tag), [i for i in root1.children])
        chs2 = filter(lambda x: isinstance(x, element.Tag), [i for i in root2.children])

        seq1 = []
        for i in chs1:
            seq1.append(len(filter(lambda x: isinstance(x, element.Tag), [j for j in i.children])))

        seq2 = []
        for i in chs2:
            seq2.append(len(filter(lambda x: isinstance(x, element.Tag), [j for j in i.children])))

        for i in range(0, len(seq1)):
            if seq1[i] == 0 or seq2[i] == 0:
                ts1 = Segment(chs1[i])
                if ts1.get_cost() > 0.1:
                    acc1.append(ts1)
                ts2 = Segment(chs2[i])
                if ts2.get_cost() > 0.1:
                    acc2.append(ts2)
            elif cosine_similarity(str(chs1[i]), str(chs2[i])) > treshold:
                pass
            elif seq1[i] == seq2[i]:
                dual_search(chs1[i], chs2[i], acc1, acc2, treshold)
            else:
                ts1 = Segment(chs1[i])
                if ts1.get_cost() > 0.1:
                    acc1.append(ts1)
                ts2 = Segment(chs2[i])
                if ts2.get_cost() > 0.1:
                    acc2.append(ts2)


def analyze(docs):
    """
    Merges trees

    """

    trees = map(lambda x: search(prep(open(x).read()),[]), docs)
    tree1 = trees[0]
    tree2 = trees[1]

    print "Overal similarity:"
    print multi_sequence_sim(tree1, tree2)

    for i in range(0, min(len(tree1), len(tree2))):
        arr, res = sequence_sim(tree1[i], tree2[i])
        al1, al2 = aligment(tree1[i], tree2[i], arr)
        print res
        print al1, al2


def tree_segmentation(base, treshold=0.9):
    if len(base) < 2:
        return None

    acc1 = []
    acc2 = []
    dual_search(base[0], base[1], acc1, acc2, treshold)

    return [acc1, acc2]

