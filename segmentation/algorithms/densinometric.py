from bs4 import element
import re


def difference(density, other_density):
    if density == 0.0 or other_density == 0.0:
        return 0.0
    else:
        return abs(density - other_density) / max(density, other_density)


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