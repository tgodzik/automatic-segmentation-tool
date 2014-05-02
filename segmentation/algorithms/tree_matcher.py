__author__ = 'Tomasz Godzik'

import numpy as np

s = 'ACGGTAG'
t = 'CCTAAG'

n = len(s)
m = len(t)

arr = np.zeros((m + 1, n + 1), dtype=np.int)

arr[0, 0] = 0

sim_mat = {
    "A": {"A": 2, "C": -1, "G": 1, "T": -1},
    "C": {"A": -1, "C": 2, "G": -1, "T": 1},
    "G": {"A": 1, "C": -1, "G": 2, "T": -1},
    "T": {"A": -1, "C": 1, "G": -1, "T": 2}, }

gap_score = -2

for j in range(0, n + 1):
    arr[0, j] = gap_score * j

for i in range(0, m + 1):
    arr[i, 0] = gap_score * i

for i in range(1, m + 1):
    for j in range(1, n + 1):
        match = arr[i - 1, j - 1] + sim_mat[s[j - 1]][t[i - 1]]
        gaps = arr[i, j - 1] + gap_score
        gapt = arr[i - 1, j] + gap_score
        arr[i, j] = max(match, gaps, gapt)

print arr

i = m
j = n

t_aln = ""
s_aln = ""

while i > 0 and j > 0:
    if (arr[i, j] - sim_mat[s[j - 1]][t[i - 1]]) == arr[i - 1, j - 1]:
        t_aln = t[i - 1] + t_aln
        s_aln = s[j - 1] + s_aln
        i -= 1
        j -= 1
    elif (arr[i, j] - gap_score) == arr[i, j - 1]:
        s_aln = s[j - 1] + s_aln
        t_aln = '_' + t_aln
        j -= 1
    elif (arr[i, j] - gap_score) == arr[i -1, j]:
        s_aln = '_' + s_aln
        t_aln = t[i - 1] + t_aln
        i -= 1
    else:
        print "error"

while j > 0:
    s_aln = s[j-1] + s_aln
    t_aln = '_' + t_aln
    j -= 1

while i > 0:
    s_aln = '_' + s_aln
    t_aln = t[i-1] + t_aln
    i -= 1


print t_aln,s_aln