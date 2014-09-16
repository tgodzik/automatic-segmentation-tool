from segmentation.algorithms.functions import cosine_similarity
import re
from pymongo import MongoClient


def simple_measure(segmented, name):
    """
    Checks whether a segment is similar to a previously marked reference segment set.
    @param segmented: segment
    @param name: name of the file being analyzed
    @rtype bool
    @return whether they are similar.
    """

    client = MongoClient()
    reference_set = client.segmentation.reference_set

    # set of reference words
    ref_seg = set(reference_set.find_one({"name": name})["segment"])

    reg = "[^\W\d_]+"
    found = set(re.findall(reg, segmented.text(), re.UNICODE))

    # print (ref_seg - found) | (found - ref_seg)
    tp = float(len(ref_seg & found))
    fp = float(len(ref_seg) - tp)
    fn = float(len(found) - tp)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    if precision + recall == 0.0:
        return 0.0

    f1 = 2 * precision * recall / (precision + recall)

    return f1 > 0.8


def comulative(measured_set):
    """
    Returns f1 score using above functions
    @param measured_set:
    @return:
    """

    return float(sum(measured_set)) / float(len(measured_set))


