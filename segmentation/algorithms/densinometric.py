from bs4 import element
import re


def calculate_density(text, max_line=80):
    regexp = "[^\W\d_]+"
    sum_len = len(text)
    lines = int(sum_len / max_line)
    if lines > 0:
        r = max_line * lines
        reduced_text = text[0:r]
        found = re.findall(regexp, reduced_text, re.UNICODE)
        word_density = float(len(found)) / float(lines)
    else:
        found = re.findall(regexp, text, re.UNICODE)
        word_density = float(len(found))

    return word_density


def max_density(tag):
    densities = []
    for i in tag.contents:
        if isinstance(i, element.NavigableString):
            densities.append(calculate_density(unicode(i)))
        else:
            densities.append(max_density(i))

    if len(densities) > 0:
        return max(densities)
    else:
        return 0.0


def min_density(tag):
    densities = []
    for i in tag.contents:
        if isinstance(i, element.NavigableString):
            densities.append(calculate_density(unicode(i)))
        else:
            densities.append(min_density(i))

    densities = filter(lambda x: x != 0.0, densities)
    if len(densities) > 0:
        return min(densities)
    else:
        return 0.0


def word_densities(tag):
    densities = []
    for i in tag.contents:
        if isinstance(i, element.NavigableString):
            densities.append(calculate_density(unicode(i)))
        else:
            densities.extend(word_densities(i))
    densities = filter(lambda x: x != 0.0, densities)
    return densities


def average_density(tag):
    ds = word_densities(tag)
    if len(ds) == 0:
        return 0.0
    return sum(ds) / float(len(ds))