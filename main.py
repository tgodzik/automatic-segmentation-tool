import segmentation
import os
import time
from segmentation.algorithms.densinometric import max_density


def check_files(dn):
    ret = set()
    for _, _, files in os.walk(dn):
        for f in files:
            ret.add(f[2:])
    return ret


if __name__ == "__main__":


    # specify pages to test
    base = "/home/tomasz/Documents/master_thesis/test_data/"

    fileset = check_files(base)
    
    # fileset = {"9gag.com.html", "agh.edu.pl.html", "brw.pl.html", "caranddriver.com.html",
    # "craigslist.com.html", "disney.pl.html", "dobreprogramy.pl.html"}
    # fileset = {"komiks.wp.pl.html"}
    base = "/home/tomasz/Documents/master_thesis/test_data/"

    segmented_simple = []

    segmented_fuzzy = []

    start = time.time()
    for i in fileset:

        files = ["a." + i, "b." + i, "c." + i]
        print segmentation.multi_sequence_sim(base+files[0], base+files[1])

        files = filter(lambda x: os.path.exists(base + x), files)
        
        # open all needed files
        pages = [open(base + f).read() for f in files]

        # strip form useless tags and change to segments
        ready = map(lambda x: segmentation.prep(x), pages)

        all_segs = segmentation.tree_segmentation(ready)
        
        # print all_segs
        # for a in all_segs:
            # print max_density(a[0].tags[0]), a[0].tags[0].name, a[0].tags[0].attrs
            # print max_density(a[1].tags[0]), a[1].tags[0].name, a[1].tags[0].attrs
        # visualize
        # for i in range(0, len(segmented)):
        # segmentation.visualize(segmented[i], "./tmp/" + files[i])

        # load reference pages and measure
        if len(all_segs[0]) > 0:
            for ii in range(0, len(all_segs)):
                simpl = segmentation.simple_measure(all_segs[ii][0], files[ii])
                fuzz = segmentation.fuzzy_measure(all_segs[ii][0], files[ii])
                print files[ii], simpl, fuzz
                segmented_simple.append(simpl)
                segmented_fuzzy.append(fuzz)
    print "Time : ", time.time() - start
    print segmentation.comulative(segmented_simple)
    print segmentation.comulative_fuzzy(segmented_fuzzy)
