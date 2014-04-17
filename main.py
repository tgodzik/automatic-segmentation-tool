
# functionalize it
from segmentation import block_fusion, measure
import json


def algorithm_block_fusion(numbers):
    numbers = map(str, numbers)

    files = ["./pages/page"+num+".html" for num in numbers]

    print "Analyzing files " + ",".join(numbers)

    checked = block_fusion.segment(files, treshold=4.0)

    # close files
    ref = [json.load(open("reference/segments"+num+".json")) for num in numbers]

    to_check = [map(lambda x: str(x).decode('utf-8'), i) for i in checked]

    print "Measuring performance"

    for i in range(0, len(ref)):
        results = measure([0], ref[i], to_check[i])
        print str(numbers[i]) + " - " + str(results)


if __name__ == "__main__":
    algorithm_block_fusion([1,2,3])