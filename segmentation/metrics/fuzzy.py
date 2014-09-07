from segmentation.algorithms.functions import cosine_similarity
import re
from pymongo import MongoClient


def compare(segment, ref_segment):
    """
    Checks if a segment is equal to another
    @param segment: one segment
    @type segment: set of string
    @param ref_segment: second segmment
    @type ref_segment: set of string
    @return: value between o and 1 representing similarity
    """
    return cosine_similarity(segment, ref_segment)


def fuzzy_measure(segmented, name):
    """
    Returns fuzzy similarity index between pages
    @type segmented: segment.Segment
    @param segmented: a list of Segment type objects representing segments found by algorithm
    @type name: string
    @param name: name of the file being analyzed
    @rtype double
    @return similarity between set of Segments and a set of refrence segments from database
    """

    client = MongoClient()
    reference_set = client.segmentation.reference_set
    ref_seg = set(reference_set.find_one({"name": name})["segment"])

    reg = "[^\W\d_]+"
    found = set(re.findall(reg, segmented.text(), re.UNICODE))

    return compare(found, ref_seg)


def fuzzy_f1_score(measured_set):
    """
    Returns f1 score using above functions
    @param measured_set:
    @return:
    """
    tp = float(sum(measured_set))

    fp = float(len(measured_set) - tp)
    fn = float(len(measured_set) - tp)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    # F1
    if tp == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)