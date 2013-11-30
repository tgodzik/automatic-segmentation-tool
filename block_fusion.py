__author__ = 'Tomasz Godzik'

from bs4 import BeautifulSoup
import re
from functools import reduce

html_doc = open("html_data/katowice.html").read()

soup = BeautifulSoup(html_doc)

max_line = 80

#for link in soup.find_all('a'):
#    print(link.get('href'))

for i in soup.find_all('script'):
    i.decompose()

#print(soup.prettify())
regexp = "[a-zA-Z0-9ąęółśżźćńĘĄŁÓŚŻŹĆŃ]+"


def density(text):
    sum_len = len(text)
    lines = int(sum_len / max_line)
    # reduce(lambda x, y: len(x) + len(y), b)+len(b)-1
    if lines > 0:
        r = max_line*lines
        reduced_text = text[0:r]
        found = re.findall(regexp, reduced_text, re.UNICODE)
        return len(found)/lines
    else:
        found = re.findall(regexp, text, re.UNICODE)
        return len(found)


#check why not everything gets read
for i in soup.find_all():
    if len(i.text) > 0 and not i.findChild():
        tmp = i.text
        # check if it is only whitespaces
        tmp = re.sub("[\s]+", " ", tmp)
        print(tmp, "[den]" + str(density(tmp)))