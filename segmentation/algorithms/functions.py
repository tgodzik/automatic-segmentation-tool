import math
import re
from bs4 import BeautifulSoup
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

    # strip head
    body = soup.find("body")
    for s in body.find_all(stripped):
        s.decompose()
    return Segment(body)


def algorithm(segment, files, is_measured=False, measure_files=None, visualized=False, verbose=True, treshold=None):
    """  Main algorithm for measurement purposes.
    :param files list of tuples for measuring the performance of simple list of names

    """
    if not measure_files:
        measure_files = []

    # open all needed files
    pages = [open(f).read() for f in files]

    if verbose:
        print "Analyzing files " + ",".join(files)

    #use segmentation
    checked = segment(pages, treshold)
    #
    # #measure
    # if is_measured:
    #     # open refrence pages
    #     ref = [json.load(open(f)) for f in measure_files]
    #
    #     to_check = [map(lambda x: str(x).decode('utf-8'), i) for i in checked]
    #
    #     if verbose:
    #         print "Measuring performance"
    #
    #     for i in range(0, len(ref)):
    #         results = measure([0, 1], ref[i], to_check[i])
    #         if verbose:
    #             print str(files[i]) + " - " + str(results)
    #
    # #visualize
    # if visualized:
    #     for i in range(0, len(checked)):
    #         visualize(checked[i], "result{index}.html".format(index=i))

    return checked

