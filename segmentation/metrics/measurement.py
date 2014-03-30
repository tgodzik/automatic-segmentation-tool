import fuzzy_jaccard
import simple

mdict = {0: fuzzy_jaccard.index, 1: simple.index, "fuzzy": fuzzy_jaccard.index, "simple": simple.index}


def measure(functions, entry_set, page):

    def generate():
        for f in functions:
            yield max([mdict[f](j, page) for j in entry_set])

    return [i for i in generate()]