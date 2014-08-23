from segmentation.algorithms.functions import cosine_similarity
import re
from pymongo import MongoClient


def belong(segment, ref_segments):
    """
    Checks if a segment is in a list of reference segments.
    @param segment: one segment set of words
    @type segment: set of string
    @param ref_segments: a list of refernce segments
    @type ref_segments: list of set of string
    @return: 1 if match was found or 0 otherwise
    """
    similarities = [cosine_similarity(i, segment) for i in ref_segments]
    return max(similarities) > 0.8


def simple_measure(segmented, name):
    """
    Returns similarity index between pages
    @type segmented: list of Segment
    @param segmented: a list of Segment type objects representing segments found by algorithm
    @type name: string
    @param name: name of the file being analyzed
    @rtype double
    @return similarity between set of Segments and a set of refrence segments from database
    """

    client = MongoClient()
    reference_set = client.segmentation.reference_set
    refs = reference_set.find_one({"name": name})["segments"]
    ref_sets = map(lambda x: set(x), refs)

    if len(segmented) == 0:
        if len(ref_sets) == 0:
            return 1.0
        else:
            return 0.0

    reg = "[^\W\d_]+"
    found = map(lambda x: set(re.findall(reg, x.text(), re.UNICODE)), segmented)

    measured_page = [belong(segment, ref_sets) for segment in found]

    tp = float(sum(measured_page))
    fp = float(len(found) - tp)
    fn = float(len(ref_sets) - tp)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    # jaccard
    # return sum(measured_page) / float(len(segmented) + len(ref_sets) - sum(measured_page))

    # F1
    return 2 * precision * recall / (precision + recall)


