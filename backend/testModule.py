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