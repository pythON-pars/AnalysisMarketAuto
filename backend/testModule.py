"""
    This file is only for testing modules or algorithms.
    It does not carry any semantic load.
"""

import hashlib
def file_as_bytes(file):
    with file:
        return file.read()

# print(hashlib.md5(file_as_bytes(open("UrlAuto.db", 'rb'))).hexdigest())
# print(type(file_as_bytes(open("UrlAuto.db", 'rb'))))

def testF():
    with open("UrlAuto.db", 'rb') as file:
        s = hashlib.md5(file.read()).hexdigest()
        print(s)

# testF()

from json import load, dump

s = {
    "md5sum-UrlAuto.db" : 'ba420bbc3b55aa55126dc795ef684b98'
}

# with open("Q.json", 'w') as qJson:
#     dump(s, qJson, indent=2)

def __databaseCheck():
    import hashlib
    
    file = "UrlAuto.db"

    checkSum = None
    with open(file, 'rb') as file:
        checkSum = hashlib.md5(file.read()).hexdigest()

    with open("Q.json") as qJson:
        src = load(qJson)

    if src["md5sum-UrlAuto.db"] == checkSum:
        return True

s = __databaseCheck()

print(s)