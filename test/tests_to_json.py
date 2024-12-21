from pathlib import Path
import os
import json

folder_path = Path("/Users/anuprovabhowmik/Downloads/cs466_nussinov-main/test")
test_data = []
for item in folder_path.iterdir():
    if item.is_file() and item.suffix == '.dbn':  
        with open(item, 'r') as file:
            content = file.readlines()

            test_data.append({"Name": item.name,
                              "Sequence": content[3].strip(),
                              "Structure": content[4].strip()
            })

with open('tests.json', 'w') as json_file:
    json.dump(test_data, json_file, indent=4)
