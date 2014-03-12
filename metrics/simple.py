from Levenshtein import distance
import json


# TODO change metric not to include whitespace


def belong(segment, ref_segments, tolerance=0.1):
    """
    Checks if a segment is in list of refrence segments.
    Value is 0 or 1
    """
    segment_len = len(segment)
    distances = [float(distance(i, segment)) for i in ref_segments]
    return min(distances) - tolerance*segment_len < 0.0


def index(refrence, compared):
    """
    Returns similarity index between pages metrics.
    """
    ref = json.loads(refrence)
    test = json.loads(compared)
    for page in ref.keys():
        measured_page = [belong(segment, ref[page]) for segment in test[page]]
        yield sum(measured_page)/ float( len(measured_page) + len(ref[page]) - sum(measured_page))