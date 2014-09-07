import segmentation
import os


def check_files(dn):
    ret = set()
    for _, _, files in os.walk(dn):
        for f in files:
            ret.add(f[2:])
    return ret


if __name__ == "__main__":

    # specify pages to test
    base = "/home/tomasz/Documents/master_thesis/test_data/"

    # fileset = check_files(base)
    fileset = {"northfish.pl.html"}

    segmented_simple = []

    segmented_fuzzy = []

    for i in fileset:

        files = ["a." + i, "b." + i, "c." + i]
        files = filter(lambda x: os.path.exists(base + x), files)
        # open all needed files
        pages = [open(base + f).read() for f in files]

        # strip form useless tags and change to segments
        ready = map(lambda x: segmentation.prep(x), pages)

        all = segmentation.tree_segmentation(ready)

        for i in all:
            print i[0]

        # visualize
        # for i in range(0, len(segmented)):
        # segmentation.visualize(segmented[i], "./tmp/" + files[i])

        # load reference pages and measure
        for ii in range(0, len(all)):
            simpl = segmentation.simple_measure(all[ii][0], files[ii])
            fuzz = segmentation.fuzzy_measure(all[ii][0], files[ii])

            segmented_simple.append(simpl)
            segmented_fuzzy.append(fuzz)

    print segmentation.simple_f1_score(segmented_simple)
    print segmentation.fuzzy_f1_score(segmented_fuzzy)