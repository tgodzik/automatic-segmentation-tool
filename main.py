
# functionalize it
from segmentation.metrics import simple

refJson = """
{"page1" : ["aaaaaaaaaaaaa", "bbbb", "cccc"]}
"""

testJson = """
{"page1" : ["aaaaaaaaaaaaaa","bbbbcccc"]}
"""

testJson2 = """
{"page1" : ["aa","aa","bb","bb","cc","cc"]}
"""

for i in simple.index(refJson, testJson):
    print i