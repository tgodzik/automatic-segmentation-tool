
# functionalize it
from segmentation import block_fusion, measure
import json


def algorithm_block_fusion(numbers, is_measured=False):
    numbers = map(str, numbers)

    files = [open("./pages/page"+num+".html").read() for num in numbers]

    print "Analyzing files " + ",".join(numbers)

    checked = block_fusion.segment(files, treshold=0.5)

    if is_measured:
        # close files
        ref = [json.load(open("reference/segments"+num+".json")) for num in numbers]

        to_check = [map(lambda x: str(x).decode('utf-8'), i) for i in checked]

        print "Measuring performance"

        for i in range(0, len(ref)):
            results = measure([0, 1], ref[i], to_check[i])
            print str(numbers[i]) + " - " + str(results)
    else:
        for i in checked:
            for seg in i:
                print seg.density, seg

if __name__ == "__main__":
    algorithm_block_fusion([1], True)