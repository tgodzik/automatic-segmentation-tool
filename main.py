import segmentation
import os


def check_files(dn):
    ret = set()
    for _, _, files in os.walk(dn):
        for f in files:
            ret.add(f[2:])
    return ret


if __name__ == "__main__":

    totals = 0.0
    totalf = 0.0
    j = 0

    # specify pages to test
    base = "/home/tomasz/Documents/master_thesis/test_data/"

    fileset = check_files(base)
    # fileset = {"northfish.pl.html"}
    for i in fileset:

        j += 2

        files = ["a." + i, "b." + i]

        # open all needed files
        pages = [open(base + f).read() for f in files]

        # strip form useless tags and change to segments
        ready = map(lambda x: segmentation.prep(x), pages)


            # # for i in ready:
            # #     print i.tags[0].prettify()
            # # apply algorithms - modular part
            # segmented = segmentation.block_fusion(ready, 0.05)
        segmented = segmentation.tree_segmentation(ready)

        # print len(segmented[0])
        # for i in segmented[0]:
        #     print i.density()
        #     print i.tags[0].name
        #     print i.word_set()

        # print len(segmented[1])
        # for i in segmented[1]:
        #     print i.density()
        #     print i.tags[0].name
        #     print i.word_set()

        # print len(segmented[2])
        # for i in segmented[2]:
        #     print i.density()
        #     print i.tags[0].name
        #     print i.word_set()
        # visualize
        # for i in range(0, len(segmented)):
        #     segmentation.visualize(segmented[i], "./tmp/" + files[i])

        # load reference pages and measure
        for ii in range(0, len(segmented)):
            simpl = segmentation.simple_measure(segmented[ii], files[ii])
            fuzz = segmentation.fuzzy_measure(segmented[ii], files[ii])
            totals += simpl
            totalf += fuzz
            # print files[ii] + " - simple: ", simpl
            # print files[ii] + " - fuzzy: ", fuzz

    print "Total simple : ", totals / float(j)
    print "Total fuzzy : ", totalf / float(j)