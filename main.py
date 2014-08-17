import segmentation
import json
from pymongo import MongoClient

if __name__ == "__main__":

    # specify pages to test
    base = "/home/tomasz/Documents/master_thesis/test_data/"
    files = ["a.brw.pl.html", "b.brw.pl.html"]

    # open all needed files
    pages = [open(base + f).read() for f in files]

    # strip form useless tags and change to segments
    ready = map(lambda x: segmentation.prep(x), pages)

    # apply algorithms - modular part
    segmented = segmentation.block_fusion(ready)

    # visualize
    for i in range(0, len(segmented)):
        segmentation.visualize(segmented[i], "./tmp/" + files[i])

    # load reference pages and measure
    for i in range(0, len(segmented)):
        segmentation.simple_measure(segmented[i], files[i])
