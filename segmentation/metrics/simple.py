from Levenshtein import distance
import json


# TODO change metric not to include whitespace


def belong(segment, ref_segments, tolerance=0.1):
    """
    Checks if a segment is in list of reference segments.
    Value is 0 or 1
    """
    segment_len = len(segment)
    distances = [float(distance(i, segment)) for i in ref_segments]
    return min(distances) - tolerance * segment_len < 0.0


def index(segmented, refrence):
    """
    Returns similarity index between pages
    """
    measured_page = [belong(segment, refrence) for segment in segmented]
    return sum(measured_page) / float(len(segmented) + len(refrence) - sum(measured_page))