import math
import re
from bs4 import BeautifulSoup, element
from .segment import Segment


def word_count(text):
    regexp = "[^\W\d_]+"
    found = re.findall(regexp, text, re.UNICODE)
    return len(found)


def max_wordcount(tag):
    counts = []
    for i in tag.contents:
        if isinstance(i, element.NavigableString):
            counts.append(word_count(unicode(i)))
        else:
            counts.append(max_wordcount(i))

    if len(counts) > 0:
        return max(counts)
    else:
        return 0.0


def min_wordcount(tag):
    counts = []
    for i in tag.contents:
        if isinstance(i, element.NavigableString):
            counts.append(word_count(unicode(i)))
        else:
            counts.append(min_wordcount(i))

    counts = filter(lambda x: x != 0.0, counts)
    if len(counts) > 0:
        return min(counts)
    else:
        return 0.0


def wordcounts(tag):
    counts = []
    for i in tag.contents:
        if isinstance(i, element.NavigableString):
            counts.append(word_count(unicode(i)))
        else:
            counts.extend(wordcounts(i))

    counts = filter(lambda x: x != 0.0, counts)

    return counts


def average_wordcount(tag):
    ds = wordcounts(tag)
    if len(ds) == 0:
        return 0.0
    return sum(ds) / float(len(ds))


def cosine_similarity(doc1, doc2):
    """
    Calculates cosine similarity between 2 html documents.
    @type doc1: set of string
    @param doc1: first document as a set of words
    @type doc2: set of string
    @param doc2: second document as a set of words
    @rtype double
    @return: calculates similarity as a double
    """
    if len(doc1) == 0 or len(doc2) == 0:
        return 0.0
    # dice
    main_vector = set(doc1.union(doc2))

    vector1 = map(lambda x: x in doc1, main_vector)

    vector2 = map(lambda x: x in doc2, main_vector)

    dot_product = sum([vector1[i] * vector2[i] for i in range(0, len(vector1))])

    norm_vector1 = math.sqrt(sum(vector1))

    norm_vector2 = math.sqrt(sum(vector2))

    return dot_product / (norm_vector1 * norm_vector2)


def prep(html_doc):
    """Removes unnecessary tags.
    @param html_doc: document to be prepared
    @type html_doc: str
    @return body tag without comments and unnecessary tags.
    @rtype bs4.element.Tag
    """
    doc = re.sub("[\s]+", " ", html_doc)
    soup = BeautifulSoup(doc)

    stripped = ["script", "noscript", "link", "iframe", "meta", "style"]

    body = soup.find("body")
    for s in body.find_all(stripped):
        s.decompose()

    comments = soup.findAll(text=lambda text: isinstance(text, element.Comment))
    [comment.extract() for comment in comments]

    return body


