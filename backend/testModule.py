"""
    This file is only for testing modules or algorithms.
    It does not carry any semantic load.
"""

import sqlite3

def clad():
    dataRes = sqlite3.connect("result.db")
    sqlRes =  dataRes.cursor()

    sum = sqlRes.execute("SELECT * FROM controlSum").fetchall()[0]
    dataRes.commit()

    if sum[0] == "fb57df74ff743b611fc298af3bf3a7ec":
        return True

    print(sum[0])

print(clad())
