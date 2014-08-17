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
    @return: from 0 to 1 based on maximum similarity
    """
    similarities = [cosine_similarity(i, segment) for i in ref_segments]
    return max(similarities)


def fuzzy_measure(segmented, name):
    """
    Returns fuzzy similarity index between pages
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

    reg = "[^\W\d_]+"
    found = map(lambda x: set(re.findall(reg, x.text(), re.UNICODE)), segmented)
    measured_page = [belong(segment, ref_sets) for segment in found]
    return sum(measured_page) / (len(ref_sets) + len(found) - sum(measured_page))