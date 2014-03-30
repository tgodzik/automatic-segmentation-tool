__author__ = 'Tomasz Godzik'

from bs4 import BeautifulSoup
from bs4 import NavigableString
import re

html_doc = open("html_data/katowice.html").read()

soup = BeautifulSoup(html_doc)

max_line = 80
treshold = 1.5
#for link in soup.find_all('a'):
#    print(link.get('href'))

for i in soup.find_all('script'):
    i.decompose()


def strip_tags(bsoup, tag_names):
    for tag in bsoup.find_all():
        if tag.name in tag_names:
            s = tag.text
            tag.replaceWith(s)

    return bsoup


regexp = "[a-zA-Z0-9ąęółśżźćńĘĄŁÓŚŻŹĆŃ]+"

soup = strip_tags(soup, ['a', 'br', 'b'])
#f = open("tmp.txt", "w")
#f.write(soup.prettify())
#f.close()


def density(text):
    sum_len = len(text)
    lines = int(sum_len / max_line)
    # reduce(lambda x, y: len(x) + len(y), b)+len(b)-1
    if lines > 0:
        r = max_line * lines
        reduced_text = text[0:r]
        found = re.findall(regexp, reduced_text, re.UNICODE)
        return len(found) / lines
    else:
        found = re.findall(regexp, text, re.UNICODE)
        return len(found)


blocks = []
#Trzeba zmienić by nie tylko prosto sprawdzał czy ma dzieci, to nie działa, bo są czasem w tekście a.
#Pewnie trzeba będzie przeparsować.
for i in soup.find_all():
    if len(i.text) > 0:
        children = i.findChild()
        if not children:
            tmp = i.text
            tmp = re.sub("[\s]+", " ", tmp)
            if len(tmp) > 1:
                #print(tmp, " : " + str(density(tmp)))
                blocks.append((tmp, density(tmp)))


change = True


def join(a, b):
    tmp = a[0] + " " + b[0]
    return tmp, density(tmp)


while change:
    change = False
    i = 0
    while i < (len(blocks)-2):
        if blocks[i][1] - blocks[i+1][1] < treshold:
            joined = join(blocks[i], blocks[i+1])
            blocks.remove(blocks[i])
            blocks.remove(blocks[i+1])
            blocks.append(joined)
            change = True
        i += 1

for b in blocks:
    print(b)