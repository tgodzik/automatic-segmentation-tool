# coding=utf-8
import os
import json
from pymongo import MongoClient
import re
from bs4 import BeautifulSoup

dname = "/home/tomasz/Documents/master_thesis/test_marked"

client = MongoClient()

coll = client.segmentation.reference_set


def save_files(dn):
    for root, dirs, files in os.walk(dn):
        for f in files:
            jslist = json.load(open(dn + "/" + f))

            replaced = map(lambda x: BeautifulSoup(x).text, jslist)

            reg = "[^\W\d_]+"

            found = map(lambda x: (re.findall(reg, x, re.UNICODE)), replaced)
            if len(found) > 0:
                to_save = {
                    "name": f.replace(".json", ".html"),
                    "segment": found[0]
                }
            else:
                to_save = {
                    "name": f.replace(".json", ".html"),
                    "segment": found
                }

            coll.insert(to_save)


save_files(dname)