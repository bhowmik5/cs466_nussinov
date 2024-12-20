#Imports
import numpy as np
import pandas as pd
from pathlib import Path
import random
import time

def nussinov(sequence):
    pairings = {'A':'U','U':'A','C':'G','G':'C'}


    l = len(sequence)
    D = np.zeros((l, l))
    backpointers = [[[] for _ in range(l)] for _ in range(l)]
    for i in range(1, l): # Length of search
        for j in range(l - i): #Left index
            k = i + j #Right index
            a = D[j + 1][k - 1]
            ascore = 0
            for t in range((i-1)//2): # Minimum loop distance 2
                if sequence[j+t] in pairings and pairings[sequence[j+t]] == sequence[k-t]:
                    ascore += 1
                else:
                    break
            maxt = 1
            for t in range(1, ascore + 1):
                tscore = D[j + t][k - t] + 2 * t - 1 # Score continuous pairings with factor of 2
                if tscore > a:
                    maxt = t
                    a = tscore
            b = D[j + 1][k]
            c = D[j][k - 1]
    
            max_score = max(a, b, c)
            for m in range(j+2, k-1):
                max_score = max(D[j][m] + D[m+1][k], max_score) # Counting this actually reduces accuracy in all cases. We can discuss why in report.

            D[j][k] = max_score
            if a == max_score:
                backpointers[j][k].append((j + maxt, k - maxt))
            elif b == max_score:
                backpointers[j][k].append((j + 1, k))
            elif c == max_score:
                backpointers[j][k].append((j, k - 1))
            maxmin = 0
            maxm = -1
            for m in range(j+2, k-1):
                if D[j][m] + D[m+1][k] == max_score:
                    if min(D[j][m], D[m+1][k]) > maxmin:
                        maxmin = max(maxmin, min(D[j][m], D[m+1][k])) # Select a maximal split to reduce meaningless traversal
                        maxm = m
            if maxm != -1:
                backpointers[j][k].append((j, maxm, maxm + 1, k))

    def backtracing(i, j):
        my_structs = []
        for back_pointer in backpointers[i][j]:
            if len(back_pointer) == 2:
                i1, j1 = back_pointer
                child_structs = backtracing(i1, j1)
                if len(child_structs) == 0 and D[i][j] > D[i1][j1]:
                    stack_list = []
                    for d in range(i1-i):
                        stack_list.append((i+d, j-d))
                    my_structs.append(stack_list)
                for child_struct in child_structs:
                    if D[i][j] > D[i1][j1]:
                        stack_list = []
                        for d in range(i1-i):
                            stack_list.append((i+d, j-d))
                        my_structs.append(child_struct + stack_list)
                    else:
                        my_structs.append(child_struct)
            else:
                i1, j1, i2, j2 = back_pointer
                left_structs = backtracing(i1, j1)
                right_structs = backtracing(i2, j2)
                for left_struct in left_structs:
                    for right_struct in right_structs:
                        my_structs.append(left_struct + right_struct)
        return my_structs
    structures = backtracing(0, l-1)
    
    outputList = []
    for structure in structures:
        secondary_structure = ['.'] * l
        for pair in structure:
            i, j = pair
            secondary_structure[i] = '('
            secondary_structure[j] = ')'
        secondary_structure = ''.join(secondary_structure)
        if secondary_structure not in outputList:
            outputList.append(secondary_structure)
    return outputList

sequence = input("Enter your RNA sequence: ")
print(nussinov(sequence))
