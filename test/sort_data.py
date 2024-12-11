from pathlib import Path
import os

folder_path = Path("/Users/anuprovabhowmik/Downloads/test_data")


for item in folder_path.iterdir():
    if item.is_file() and item.suffix == '.dbn':  
        with open(item, 'r') as file:
            content = file.readlines()

            #Removes files with bp length over 50
            for thing in content:
                if thing.strip().split(": ")[0] == "#Length":
                    length = int(thing.strip().split(": ")[1].strip(','))
                    print("TOO BIG", item.name)
                    break
            if length > 50:
                os.remove(item.name)
            else:
                #Removes files without base pairs
                if '(' not in content[3]:
                    os.remove(item.name)
                    print("no pairs", item.name)
                #Removes files with pseudoknots
                if '[' in content[3]:
                    os.remove(item.name)
                    print("pseudoknot", item.name)
