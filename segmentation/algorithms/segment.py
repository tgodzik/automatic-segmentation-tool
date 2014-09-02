import re
from bs4 import element
# -*- coding: utf-8 -*-


class Segment:
    """
    Represents a single HTML web segment.
    """

    regexp = "[^\W\d_]+"

    def __init__(self, tag):
        self.tags = [tag]
        self.word_density = None

    def __str__(self):
        return "".join([str(i) for i in self.tags])

    def __add__(self, other):
        self.tags.extend(other.tags)
        self.word_density = None
        return self

    def difference(self, other):
        if self.density() == 0.0 or other.density() == 0.0:
            return 0.0
        else:
            return abs(self.density() - other.density()) / max(self.density(), other.density())

    def density(self):
        return self.word_density or self.calculate_density()

    @staticmethod
    def get_str(a):
        if isinstance(a, element.Tag):
            return a.text
        else:
            return unicode(a)

    def calculate_density(self, max_line=80):
        """
        Get the current text density of the segment.
        @todo possible time improvements
        @param max_line: maimum line length
        @return: current density
        """
        text = "".join([self.get_str(i) for i in self.tags])

        sum_len = len(text)
        lines = int(sum_len / max_line)
        if lines > 0:
            r = max_line * lines
            reduced_text = text[0:r]
            found = re.findall(Segment.regexp, reduced_text, re.UNICODE)
            self.word_density = float(len(found)) / float(lines)
        else:
            found = re.findall(Segment.regexp, text, re.UNICODE)
            self.word_density = float(len(found))

        return self.word_density

    def text(self):
        return "".join([self.get_str(i) for i in self.tags])

    def word_set(self):
        return set(re.findall(Segment.regexp, self.text(), re.UNICODE))