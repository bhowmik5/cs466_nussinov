from pathlib import Path
import os
import json

folder_path = Path("/media/ddas11/dd01/Anuprova/test_data/test_data")
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

print("DONE")
