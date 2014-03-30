from Levenshtein import distance
import json

# TODO change metric not to include whitespace


def belong(segment, ref_segments):
    """
    Checks if a segment is in list of refrence segments.
    Value is between 0 and 1
    """
    segment_len = len(segment)
    distances = [float(distance(i, segment)) for i in ref_segments]
    # get minimal distance, divide by the length and binarize
    return 1.0 - min(min(distances)/segment_len, 1.0)


def index(refrence, compared):
    """
    Returns similarity index between pages metrics.
    """
    ref = json.loads(refrence)
    test = json.loads(compared)
    for page in ref.keys():
        measured_page = [belong(segment, ref[page]) for segment in test[page]]
        yield 2*sum(measured_page)/(len(ref[page]) + len(test[page]))