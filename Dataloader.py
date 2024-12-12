import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import time
from random import randint

data = pd.read_csv("extended_testdb.csv")
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
userlogs = client.testdb.userlogs

print(data.dtypes)
for i in range(8):
    data.loc[i,'date'] = float(data.loc[i,'date'])
    print(data.loc[i])
    #userlogs.insert_one(data.loc[i])

for i in range(8, len(data)):
    data.loc[i, 'date'] = datetime.strptime(data.loc[i, 'date'], "%d/%m/%y").timestamp()

datadicts = data.to_dict(orient='records')

for d in datadicts:
    userlogs.insert_one(d)
    time.sleep(randint(5,60))