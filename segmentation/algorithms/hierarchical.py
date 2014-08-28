import re
from bs4 import element
from .segment import Segment
from .functions import cosine_similarity

inline_elements = ["b", "big", "i", "small", "tt", "abbr", "acronym", "cite",
                   "code", "dfn", "em", "kbd", "strong", "samp", "var", "a",
                   "bdo", "br", "img", "map", "object", "q", "script", "span",
                   "sub", "sup", "button", "input", "label", "select", "textarea"]


def word_set(tag):
    """
    Returns a set of words from tag.
    @param tag: element.Tag
    @return: set of words
    """

    reg = "[^\W\d_]+"

    if isinstance(tag, element.Tag):
        found = re.findall(reg, tag.text, re.UNICODE)
    else:
        found = re.findall(reg, unicode(tag), re.UNICODE)
    return {i.lower() for i in found}


def change_tag(x):
    """
    Changes tag to a comparable representation.
    @todo determine whether to check different types of tags i.e. formatting tags
    @param x: element
    @return: true if a tag, false otherwise
    """
    if isinstance(x, element.Tag):
        return x.name
    else:
        return "text"


def filter_tag(x):
    """
    Checks if to go into an element.
    @todo Maybe not remove text nodes
    @param x: element
    @return: true if a tag, false otherwise
    """
    if isinstance(x, element.Tag):
        if x.name in inline_elements:
            return False
        return True
    else:
        return True


def sequence_compare(sq1, sq2):
    """
    Check whether
    @param sq1:
    @param sq2:
    @return:
    """
    return sq1 == sq2


def cases(tags, treshold):
    """
    Analyze and check different cases.
    @param tags: all tags
    @param treshold: similarity threshold
    @return: pair of lists or pair of None
    """

    word_sets = map(word_set, tags)
    sequences = map(lambda one: map(change_tag, one.children), tags)

    # @todo conditions about lists
    # 1. The tags have almost same words
    if all([(cosine_similarity(word_sets[0], wsi) > treshold) for wsi in word_sets[1:]]):
        return [[] for t in xrange(len(tags))]
    # 2. The tags have no words
    elif any([(len(wsi) == 0) for wsi in word_sets]):
        return [[] for t in xrange(len(tags))]
    # 3. Tags have the same children sequences
    elif all(sequence_compare(sequences[0], seq) for seq in sequences[1:]) and (len(sequences[0]) != 0):
        return [None] * len(tags)
    # 4. Otherwise, this is a segment
    else:
        return map(lambda sg: [Segment(sg)], tags)


def concurent_search(tags, treshold):
    """
    We could also check for tag name.
    @param tags: roots of the trees
    @param treshold: maximum similarity difference
    @return:
    """
    if all([hasattr(tag, "children") for tag in tags]):

        childi = map(lambda x: filter(filter_tag, x.children), tags)

        rets = [[] for x in xrange(len(tags))]

        for i in range(0, len(childi[0])):

            # @todo if is list
            cnvs = map(lambda x: x[i], childi)
            cas = cases(cnvs, treshold)
            if cas[0] is None:
                cas = concurent_search(cnvs, treshold)

            for r, c in zip(rets, cas):
                r.extend(c)

        return rets


def filter_out(x):
    """
    Checks if a segment contains something more than links and numbers.
    POSTPROCESS
    @param x: segment object
    @return: True or False
    """

    # if x.name in ["time", "a"]:
    # return False

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

    # add cases also here
    base_tags = map(lambda x: x.tags[0], base)

    converted = cases(base_tags, treshold)

    if converted[0] is None:
        converted = concurent_search(base_tags, treshold)

    return [filter(filter_out, a) for a in converted]

