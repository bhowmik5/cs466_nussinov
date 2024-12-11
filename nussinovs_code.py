#Imports
import pandas as pd
from pathlib import Path
import os

#Set Path
folder_path = Path("/Users/anuprovabhowmik/Downloads/dbnFiles/test_data")

#Number of data points
num_rows = sum(1 for item in os.listdir(folder_path)
                     if os.path.isfile(os.path.join(folder_path, item)) and item.endswith('.dbn'))

#Initialize Dataframe
df = pd.DataFrame(index=range(num_rows), columns=["Name", "Sequence", "Recall", "Precision", "F1"])
row = 0

#Open test files
for name in folder_path.iterdir():
    if name.is_file() and name.suffix == '.dbn':  
        with open(name, 'r') as file:
            content = file.readlines()
            sequence = content[3].strip()
            actual = content[4].strip()

        #Fill in matrix
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


        #Add all possible solutions to array
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
        for structure in structures:
            secondary_structure = ['.'] * l
            for pair in structure:
                i, j = pair
                secondary_structure[i] = '('
                secondary_structure[j] = ')'
            if ''.join(secondary_structure) not in outputList:
              outputList.append("".join(secondary_structure))
        
        #Make list of pairs for test file
        stack = []
        actualPairs = []  
        for i, char in enumerate(actual):
            if char == '(':
                stack.append(i) 
            elif char == ')':
                if stack:  
                    opening_index = stack.pop()  
                    actualPairs.append((opening_index, i))

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
                if thing not in pairs:
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

            if f1 > maxf1:
                df.loc[row] = [name, item, recall, precision, f1]
                maxf1 = f1
        print(name)        
        row += 1

#Export data as spreadsheet
df.to_excel('output.xlsx', index=False)

          
