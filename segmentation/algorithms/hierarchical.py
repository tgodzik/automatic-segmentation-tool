import re
from bs4 import element
from .segment import Segment
from .functions import cosine_similarity


def word_set(tag):
    """
    Returns a set of words from tag.
    @param tag: element.Tag
    @return: set of words
    """
    reg = "[^\W\d_]+"
    found = re.findall(reg, tag.text, re.UNICODE)

    return {i.lower() for i in found}


def check_tag(x):
    """
    Checks if an element is a Tag
    @param x: element
    @return: true if a tag, false otherwise
    """
    return isinstance(x, element.Tag) and x.name not in ["time", "a"]


# check for a number of date (same as with links) objects and remove that
# check text density for desired one
# think of using precision recal


def cases(tag1, tag2, treshold):
    """
    Analyze and check different cases.
    @param tag1: first tag
    @param tag2: second tag
    @param treshold: similarity threshold
    @return: pair of lists or pair of None
    """
    ws1 = word_set(tag1)
    ws2 = word_set(tag2)

    seq1 = filter(check_tag, [j for j in tag1.children])
    seq2 = filter(check_tag, [j for j in tag2.children])

    equal_names = True
    for i, j in zip(seq1, seq2):
        equal_names = equal_names and (i.name == j.name)

    print [j.name for j in seq1]
    print [j.name for j in seq2]
    seq_len1 = len(seq1)
    seq_len2 = len(seq2)
    names1 = tag1.name
    names2 = tag2.name

    if cosine_similarity(ws1, ws2) > treshold:
        return [], []
    elif len(ws1) == 0 or len(ws2) == 0:
        return [], []
    elif equal_names and (seq_len1 == seq_len2) and (seq_len1 != 0):
        return None, None
    else:
        ts1 = Segment(tag1)
        ts2 = Segment(tag2)
        return [ts1], [ts2]


def concurent_search(tag1, tag2, treshold):
    """
    We could also check for tag name.
    @param tag1: root of the first tree
    @param tag2: root of the second tree
    @param treshold: maximum similarity difference
    @return:
    """
    if hasattr(tag1, "children") and hasattr(tag2, "children"):

        child1 = filter(check_tag, [i for i in tag1.children])
        child2 = filter(check_tag, [i for i in tag2.children])
        ret1, ret2 = [], []
        for i in range(0, len(child1)):
            a, b = cases(child1[i], child2[i], treshold)
            if a is None:
                a, b = concurent_search(child1[i], child2[i], treshold)
            ret1.extend(a)
            ret2.extend(b)

        return ret1, ret2


def filter_out(x):
    """
    Checks if a segment contains something more than links and numbers.
    @param x: segment object
    @return: True or False
    """

    if x.density() < 5.0:
        return False

    wrong = 0
    all_letters = 0

    for i in x.tags:
        reject = i.find_all(['a', 'time'])

        digit_reg = re.compile("\d", re.UNICODE)
        links_nums = sum([len(digit_reg.findall(j.text)) for j in reject])
        nums = len(digit_reg.findall(i.text))

        word_reg = re.compile("\w", re.UNICODE)
        links_all = sum([len(word_reg.findall(j.text)) for j in reject])

        all_letters += len(word_reg.findall(i.text))
        wrong += nums - links_nums + links_all

    # arbitrary 0.5
    if all_letters * 0.5 <= wrong:
        return False
    else:
        return True


def tree_segmentation(base, treshold=0.9):
    """
    Top level tree segmentation algorithm.
    @param base: list of segments to analyze
    @param treshold: similarity threshold
    @return: two lists of segments
    """
    if len(base) < 2:
        return None

    a, b = concurent_search(base[0].tags[0], base[1].tags[0], treshold)

    for i in a:
        print i
    af = filter(filter_out, a)
    bf = filter(filter_out, b)

    return [af, bf]

