from segmentation.algorithms.cosine import cosine_similarity


# @TODO check why the tree algorithm gives zeroes

def belong(segment, ref_segments):
    """
    Checks if a segment is in list of reference segments.
    Value is between 0 and 1
    """
    similarities = [cosine_similarity(i, segment) for i in ref_segments]
    return max(similarities)


def index(segmented, refrence):
    """
    Returns similarity index between 2 segmented pages.
    """
    measured_page = [belong(segment, refrence) for segment in segmented]
    return sum(measured_page)/(len(refrence) + len(segmented) - sum(measured_page))