
# functionalize it
refJson = """
{"page1" : ["aaaaaaaaaaaaa", "bbbb", "cccc"]}
"""

testJson = """
{"page1" : ["aaaaaaaaaaaaaa","bbbbcccc"]}
"""

testJson2 = """
{"page1" : ["aa","aa","bb","bb","cc","cc"]}
"""

from metrics import simple

for i in simple.index(refJson, testJson):
    print i