import re
# -*- coding: utf-8 -*-


class Segment:
    """Represents a single segment

    """
    def __init__(self, tag):
        self.tags = [tag]


class TreeSegment(Segment):
    """Class representing a single segment for tree comparing methods.

    """
    def __init__(self, tag):
        Segment.__init__(self, tag)
        self.sequence = [1]


class DensitySegment(Segment):
    """Class representing a single segment for densinometric methods.

    """

    def __init__(self, tag):
        Segment.__init__(self, tag)
        self.simplify()
        self.density = self.calculate_density()

    def __add__(self, other):
        self.tags.extend(other.tags)
        self.density = self.calculate_density()
        return self

    def __sub__(self, other):
        if self.density == 0.0 or other.density == 0.0:
            return 0.0
        return abs(self.density - other.density) / max(self.density, other.density)

    def simplify(self):
        parent = self.tags[0].parent

        if len(self.tags) == len(parent.find_all()):
            self.tags = [parent]
            self.simplify()

    def __str__(self):
        return "".join([str(i) for i in self.tags])

    def calculate_density(self, max_line=80):
        text = "".join([i.text for i in self.tags])
        regexp = "[a-zA-Z0-9ąęółśżźćńĘĄŁÓŚŻŹĆŃ]+"
        sum_len = len(text)
        lines = int(sum_len / max_line)
        if lines > 0:
            r = max_line * lines
            reduced_text = text[0:r]
            found = re.findall(regexp, reduced_text, re.UNICODE)
            return float(len(found)) / float(lines)
        else:
            found = re.findall(regexp, text, re.UNICODE)
            return float(len(found))