import re
from bs4 import element
from .segment import Segment
from .functions import cosine_similarity


class FakeTag:
    def __init__(self, name, text):
        self.name = name
        self.children = []
        self.text = text

    def find_all(self, ll):
        return []


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
    if isinstance(x, element.Tag):
        if x.name in ["time", "a"]:
            return FakeTag(x.name, x.text)
        return x
    else:
        return FakeTag("text", unicode(x))


def filter_tag(x):
    """
    Checks if an element is a Tag.
    @todo Maybe not remove text nodes
    @param x: element
    @return: true if a tag, false otherwise
    """
    if isinstance(x, element.Tag):
        if x.name in ["time", "a"]:
            return False
        return True
    else:
        return True


# check for a number of date (same as with links) objects and remove that
# check text density for desired one
# think of using precision recal


def cases(tags, treshold):
    """
    Analyze and check different cases.
    @param tags: all tags
    @param treshold: similarity threshold
    @return: pair of lists or pair of None
    """
    wss = map(word_set, tags)

    # @todo not check tag, just create a representation based on Fake Tags, used it also for ul
    # so analysis only here, also sequence matching based on aligments
    seqs = map(lambda x: map(check_tag, x.children), tags)

    equal_names = True
    for s in zip(*seqs):
        equal_names = equal_names and all([(s[0].name == si.name) for si in s[1:]])

    seq_lens = map(len, seqs)

    if all([(cosine_similarity(wss[0], wsi) > treshold) for wsi in wss[1:]]):
        return [[] for x in xrange(len(tags))]
    elif any([(len(wsi) == 0) for wsi in wss]):
        return [[] for x in xrange(len(tags))]
    elif equal_names and all([(seq_leni == seq_lens[0]) for seq_leni in seq_lens[1:]]) and (seq_lens[0] != 0):
        return [None] * len(tags)
    else:
        return map(lambda x: [Segment(x)], tags)


def concurent_search(tags, treshold):
    """
    We could also check for tag name.
    @param tags: roots of the trees
    @param treshold: maximum similarity difference
    @return:
    """
    if all([hasattr(tag, "children") for tag in tags]):

        # @todo make sure changing is correct here
        # maybe use aligment also
        childi = map(lambda x: map(check_tag, filter(filter_tag, x.children)), tags)

        rets = [[] for x in xrange(len(tags))]

        for i in range(0, len(childi[0])):
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

