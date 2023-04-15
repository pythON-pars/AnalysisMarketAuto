"""
    This file is only for testing modules or algorithms.
    It does not carry any semantic load.
"""

import json

with open('modelName.json') as model:
    src = json.load(model)

for i in src:
    din = False
    for item in i['Hyundai']:
        if item == " ":
            print(i['Hyundai'])
            din = True

    if din is True:
        i.split(' ')