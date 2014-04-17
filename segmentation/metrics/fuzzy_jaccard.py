from Levenshtein import distance


# TODO change metric not to include whitespace

def belong(segment, ref_segments):
    """
    Checks if a segment is in list of reference segments.
    Value is between 0 and 1
    """
    segment_len = len(segment)
    distances = [float(distance(i, segment)) for i in ref_segments]
    return 1.0 - min(min(distances)/segment_len, 1.0)


def index(segmented, refrence):
    """
    Returns similarity index between 2 segmented pages.
    """
    measured_page = [belong(segment, refrence) for segment in segmented]
    return sum(measured_page)/(len(refrence) + len(segmented) - sum(measured_page))