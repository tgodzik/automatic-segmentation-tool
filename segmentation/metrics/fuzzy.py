from segmentation.algorithms.functions import cosine_similarity
import re
from pymongo import MongoClient


def fuzzy_measure(segment, name):
    """
    Returns similarity F1 score between segment and previously marked reference segment set.
    @param segment: segment to be checked
    @type segment: segmentation.Segment
    @param name: name of the file being analyzed
    @rtype double
    @return how they are similar
    """

    client = MongoClient()
    reference_set = client.segmentation.reference_set

    # set of reference words
    ref_seg = set(reference_set.find_one({"name": name})["segment"])

    reg = "[^\W\d_]+"
    found = set(re.findall(reg, segment.text(), re.UNICODE))

    tp = float(len(ref_seg & found))
    fp = float(len(ref_seg) - tp)
    fn = float(len(found) - tp)

    if tp + fp == 0.0:
        return 0.0

    precision = tp / (tp + fp)

    if tp + fn == 0.0:
        return 0.0

    recall = tp / (tp + fn)

    if precision+recall == 0.0:
        return 0.0
    f1 = 2 * precision * recall / (precision + recall)

    return f1


def comulative_fuzzy(measured_set):
    """
    Returns f1 score using above functions
    @param measured_set:
    @return:
    """

    return sum(measured_set)/len(measured_set)


