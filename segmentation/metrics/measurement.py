import fuzzy_jaccard
import simple


def measure(functions, refrence, page):
    mdict = {0: fuzzy_jaccard.index, 1: simple.index, "fuzzy": fuzzy_jaccard.index, "simple": simple.index}
    return [mdict[f](page, refrence) for f in functions]