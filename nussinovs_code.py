#Imports
import pandas as pd
from pathlib import Path
import os

sequence = "CGUAGCGUGCGUCGUAGCUAGCUAGCUAGCUA"

pairings = [['A', 'U'], ['U', 'A'], ['C', 'G'], ['G', 'C']]
l = len(sequence)
D = [[0] * l for _ in range(l)]

for i in range(1, l):
    for j in range(l - i):
        k = i + j
        a = 0

        pair = []
        pair.append(sequence[j])
        pair.append(sequence[k])

        if pair in pairings:
            a = D[j + 1][k - 1] + 1

        b = D[j + 1][k - 1]
        c = D[j + 1][k]
        d = D[j][k - 1]

        max_num = max(a, b, c, d)

        for m in range(j+1, k):
            if (D[j][m] + D[m+1][k]) > max_num:
                max_num = D[j][m] + D[m+1][k]
        D[j][k] = max_num

stack = [(0, l - 1, [])]
structures = []
while stack:
    i, j, current_structure = stack.pop()
    if i >= j:
        structures.append(current_structure)
    else:
        if D[i+1][j] == D[i][j]:
            stack.append((i+1, j, current_structure))
        elif D[i][j-1] == D[i][j]:
            stack.append((i, j-1, current_structure))
        else:
            stack.append((i+1, j-1, current_structure + [(i, j)]))
            stack.append((i+1, j, current_structure))
            stack.append((i, j-1, current_structure))
    
outputList = []
max_length = max(len(arr) for arr in structures)
for structure in structures:
    if len(structure) == max_length:
        secondary_structure = ['.'] * l
        for pair in structure:
            i, j = pair
            secondary_structure[i] = '('
            secondary_structure[j] = ')'
        if ''.join(secondary_structure) not in outputList:
            outputList.append("".join(secondary_structure))
print(outputList)          
