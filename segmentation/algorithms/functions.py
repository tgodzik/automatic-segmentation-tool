import math
import re
from bs4 import BeautifulSoup, element
from .segment import Segment


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
    """Removes unnecessary tags

    """
    doc = re.sub("[\s]+", " ", html_doc)
    soup = BeautifulSoup(doc)

    stripped = ["script", "noscript", "link", "iframe", "meta", "style"]

    body = soup.find("body")
    for s in body.find_all(stripped):
        s.decompose()

    comments = soup.findAll(text=lambda text: isinstance(text, element.Comment))
    [comment.extract() for comment in comments]

    empty_tags = [""]

    while len(empty_tags) > 0:
        empty_tags = soup.findAll(lambda tag: not tag.contents and (tag.string is None or not tag.string.strip()))
        [empty_tag.extract() for empty_tag in empty_tags]

    return body


