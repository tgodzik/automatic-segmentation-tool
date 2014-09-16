import re
from bs4 import element
# -*- coding: utf-8 -*-


class SegmentClass:
    STATIC = 0
    DYNAMIC = 1


class Segment:
    """
    Represents a single HTML web segment.
    """

    regexp = "[^\W\d_]+"

    def __init__(self, tag, segment_class):
        self.tags = [tag]
        self.word_density = None
        self.index = 0.0
        self.sclass = segment_class

    def __str__(self):
        return "".join([str(i) for i in self.tags])

    def __add__(self, other):
        self.tags.extend(other.tags)
        return self

    @staticmethod
    def get_str(a):
        if isinstance(a, element.Tag):
            return a.text
        else:
            return unicode(a)

    def text(self):
        return "".join([self.get_str(i) for i in self.tags])

    def word_set(self):
        return set(re.findall(Segment.regexp, self.text(), re.UNICODE))