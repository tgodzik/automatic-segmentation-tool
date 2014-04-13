# load from file (test.html) and add to json

import json
import re

html = "pages/segments3.html"
jsonname = "pages/segments3.json"

htmlfile = open(html)

htmlpage = htmlfile.read()

segments = []
for seg in htmlpage.split("-:-"):
    segments.append(re.sub("[\s]+", " ", seg))

page = json.dump(segments, open(jsonname, "w"), indent=4)
