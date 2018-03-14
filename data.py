import pymongo
import pandas as pd
from pprint import PrettyPrinter

client = pymongo.MongoClient()
db = client.secondhand
shdb = db.shanghai

# data = list(shdb.find())
# df = pd.DataFrame(data)
# print(df)
pp = PrettyPrinter(indent = 4)
pp.pprint(shdb.find_one())

client.close()