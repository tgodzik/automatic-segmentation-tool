
refJson = """
{"page1" : ["aaaa", "bbbb", "cccc"]}
"""

testJson = """
{"page1" : ["aaaabb","bbcccc"]}
"""

testJson2 = """
{"page1" : ["aa","aa","bb","bb","cc","cc"]}
"""

from metrics import index

for i in index(refJson, testJson2):
    print i