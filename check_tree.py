__author__ = 'Tomasz Godzik'
from bs4 import BeautifulSoup
from bs4 import element

doc = open("./pages/page1.html").read()
soup = BeautifulSoup(doc)

res = [[1]]


def recurse(root, level=0):
    if hasattr(root, "children"):


        chs = filter(lambda x: isinstance(x, element.Tag), [i for i in root.children])
        count = len(chs)
        if level > 0:
            count += 1

        if count > 1:
            if len(res) <= level:
                res.append([])
            res[level].append(count)

        for i in chs:
            recurse(i, level + 1)


recurse(soup)

for i in res:
    print i
