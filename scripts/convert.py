import json
import re


html = "input.html"
jsonname = "output.json"

htmlfile = open(html)

htmlpage = htmlfile.read()

stripped = ["script", "noscript", "link", "iframe", "meta"]

segments = []

for seg in htmlpage.split("-:-"):
    for i in stripped:
        no_script = re.sub("<" + i + "(.|\n)*?>(.|\n)*?</" + i + ">", " ", seg)
    segments.append(re.sub("[\s]+", " ", no_script))

page = json.dump(segments, open(jsonname, "w"), indent=4)