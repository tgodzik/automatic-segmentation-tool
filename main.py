
# functionalize it
from segmentation import block_fusion


if __name__ == "__main__":

    checked = block_fusion.segment(["./pages/page1.html"], treshold=4.0)[0]
    print len(checked)
    f = open("segmented.html", "w")
    f.write("\n-:-\n".join([str(i) for i in checked]))
    f.close()
