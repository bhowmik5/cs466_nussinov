from pathlib import Path
import os

folder_path = Path("/Users/anuprovabhowmik/Downloads/dbnFiles/test_data")


for item in folder_path.iterdir():
    if item.is_file() and item.suffix == '.dbn':  
        with open(item, 'r') as file:
            content = file.read()
            if '(' not in content:
                os.remove(item.name)
            if '[' in content:
                print(item.name)
                os.remove(item.name)
