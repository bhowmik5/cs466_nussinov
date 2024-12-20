#Imports
import pandas as pd
from pathlib import Path
import os
import json
from nussinovs_code import *

#Set Path
folder_path = Path("/Users/anuprovabhowmik/Downloads/cs466_nussinov-main/test")

#Number of data points
with open('tests.json', 'r') as f:
    data = json.load(f)
num_rows = len(data)

#Initialize Dataframe
df = pd.DataFrame(index=range(num_rows), columns=["Name", "Sequence", "Max", "Recall", "Precision", "F1"])
row = 0

#Open test files
for thing in data:
    name = thing["Name"]
    sequence = thing["Sequence"]
    actual = thing["Structure"]
    outputList = nussinov(sequence)

    #Make list of pairs for test file
    num_pairs = 0
    stack = []
    actualPairs = []  
    for i, char in enumerate(actual):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:  
                opening_index = stack.pop()  
                actualPairs.append((opening_index, i))
                
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

    max_pairs = D[0][l-1]

    max_check = 1
    score_actual = 0
    for char in actual:
        if char == '(':
            score_actual += 1
    if max_pairs > score_actual:
        max_check = 0

    #Iterate through all possible solutions
    maxf1 = 0
    for item in outputList:
        tp, fp, fn = 0,0,0
        stack = []
        pairs = []
                    
        #Make list of pairs for possible solution
        for i, char in enumerate(item):
            if char == '(':
                stack.append(i) 
            elif char == ')':
                if stack:  
                    opening_index = stack.pop()  
                    pairs.append((opening_index, i))

        #compute rpf values and add to dataframe
        recall, precision, f1 = 0,0,0
        for thing in actualPairs:
            if thing in pairs:
                tp += 1
                pairs.remove(thing)
            else:
                fn += 1
        for thing in pairs:
            if thing not in actualPairs:
                fp += 1

        if (tp + fn) != 0:
            recall = tp/(tp+fn)

        if (tp + fp) != 0:
            precision = tp/(tp+fp)

        if (precision + recall != 0):
            f1 = 2*(precision * recall)/(precision + recall)

        if f1 >= maxf1:
            df.loc[row] = [name, item, max_check, recall, precision, f1]
            maxf1 = f1
    if(row % 100 == 0):
        print(row)
    row += 1

#Export data as spreadsheet
df.to_excel('output.xlsx', index=False)
