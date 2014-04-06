
# functionalize it
from segmentation import block_fusion


if __name__ == "__main__":

    checked = block_fusion.segment(["./pages/page1.html"], treshold=10.0)[0]
    print len(checked)
    #for i in checked:
    #    print i