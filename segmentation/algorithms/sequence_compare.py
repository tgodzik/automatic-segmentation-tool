import numpy as np


inline_elements = {"b", "big", "i", "small", "tt", "abbr", "acronym", "cite",
                   "code", "dfn", "em", "kbd", "strong", "samp", "var", "a",
                   "bdo", "br", "img", "map", "object", "q", "script", "span",
                   "sub", "sup", "button", "input", "label", "select", "textarea",
                   "cufontext", "cufon"}


def short_hand(a):
    if a in inline_elements:
        return 1
    else:
        return 2


def simple_cost(a, b, gap_score=1):
    """Simple cost of aligments
    :params a first number as string
    :params b second number as string
    :return cost as int

    """
    if a == b:
        return 0
    elif a is None:
        return short_hand(b)
    elif b is None:
        return short_hand(a)
    else:
        return short_hand(a) + short_hand(b)


def sequence_sim(a, b, cost=simple_cost):
    """Calculates similarity between 2 node sequences.
    :param a first number as string
    :param b second number as string
    :param cost cost function taking 2 parameters
    :return a tuple (numpy array of results, minimal cost)

    """

    lena = len(a)
    lenb = len(b)

    arr = np.zeros((lena + 1, lenb + 1), dtype=np.int)

    arr[0, 0] = 0

    for i in range(1, lena + 1):
        arr[i, 0] = arr[i - 1, 0] + cost(a[i - 1], None)

    for j in range(1, lenb + 1):
        arr[0, j] = arr[0, j - 1] + cost(None, b[j - 1])

    for i in range(1, lena + 1):
        for j in range(1, lenb + 1):
            match = arr[i - 1, j - 1] + cost(a[i - 1], b[j - 1])
            gapa = arr[i - 1, j] + cost(a[i - 1], None)
            gapb = arr[i, j - 1] + cost(None, b[j - 1])
            arr[i, j] = min(match, gapa, gapb)

    return arr, arr[lena, lenb]


def aligment(a, b, arr, cost=simple_cost):
    """Calculates the string aligment of 2 node sequences.
    :param a first number as string
    :param b second number as string
    :param cost cost function taking 2 parameters
    :return tuple of aligments

    """

    i = len(a)
    j = len(b)

    a_aln = []
    b_aln = []

    while i > 0 and j > 0:
        if (arr[i, j] - cost(a[i - 1], b[j - 1])) == arr[i - 1, j - 1]:
            a_aln.insert(0, a[i - 1])
            b_aln.insert(0, b[j - 1])
            i -= 1
            j -= 1
        elif (arr[i, j] - cost(a[i - 1], None)) == arr[i - 1, j]:
            a_aln.insert(0, a[i - 1])
            b_aln.insert(0, "_")
            i -= 1
        elif (arr[i, j] - cost(None, b[j - 1])) == arr[i, j - 1]:
            a_aln.insert(0, "_")
            b_aln.insert(0, b[j - 1])
            j -= 1
        else:
            print "error"

    while i > 0:
        a_aln.insert(0, a[i - 1])
        b_aln.insert(0, "_")
        i -= 1

    while j > 0:
        a_aln.insert(0, "_")
        b_aln.insert(0, b[j - 1])
        j -= 1

    return a_aln, b_aln

# seq1 = ['text', 'text', 'text', 'text', 'div', 'text', 'div', 'text', 'text', 'div', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'div', 'text', 'text', 'text']
# seq2 = ['div', 'div', 'div', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text', 'text']

seq1 = ['div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'text', 'div', 'text', 'text', 'text']
seq2 = ['div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'text', 'div', 'text', 'div', 'text', 'text']

# seq1 = ["div", "div", "ul", "ul", "div"]
# seq2 = ["div", "div", "ul", "div"]
arr, res = sequence_sim(seq1, seq2)
print arr
print aligment(seq1, seq2, arr)