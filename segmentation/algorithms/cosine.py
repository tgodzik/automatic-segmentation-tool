import re
import math


def cosine_similarity(doc1, doc2):
    regexp = "<[^>]*>|[\w\d]+"

    doc1_set = set(re.findall(regexp, doc1, re.UNICODE))
    doc2_set = set(re.findall(regexp, doc2, re.UNICODE))

    main_vector = list(doc1_set.union(doc2_set))

    vector1 = map(lambda x: x in doc1_set, main_vector)

    vector2 = map(lambda x: x in doc2_set, main_vector)

    dot_product = sum([vector1[i] * vector2[i] for i in range(0, len(vector1))])

    norm_vector1 = math.sqrt(sum(vector1))

    norm_vector2 = math.sqrt(sum(vector2))

    return dot_product / (norm_vector1 * norm_vector2)
