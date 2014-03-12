# load from file (test.html) and add to json

import json
import re

html = "segment1.html"
jsonname = "reference/page3.json"

htmlfile = open("pages/page3/segment1.html")

whole = htmlfile.read()



page = json.load(open(jsonname))

regexp = "\s+"

whole = re.sub(regexp, " ", whole)

page.append(whole)

print page[0]
#page = json.dump(page, open(jsonname, "w"))
