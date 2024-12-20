from pathlib import Path
import os

folder_path = Path("/Users/anuprovabhowmik/Downloads/cs466_nussinov-main/test")


for item in folder_path.iterdir():
    if item.is_file() and item.suffix == '.dbn':  
        with open(item, 'r') as file:
            content = file.readlines()
            #Removes files with bp length over 60
            length = 0
            for thing in content:
                if thing.strip().split(": ")[0] == "#Length":
                    length = int(thing.strip().split(": ")[1].strip(','))
                    break
            if length > 60:
                os.remove(item.name)            
            else:
                #Removes files without base pairs
                if '(' not in content[4]:
                    os.remove(item.name)
                #Removes files with pseudoknots
                if '[' in content[4]:
                    os.remove(item.name)
        
