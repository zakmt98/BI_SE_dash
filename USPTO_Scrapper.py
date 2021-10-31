import pandas as pd
from pymongo import MongoClient



client = MongoClient('localhost', 27017)
db = client['BI_project_db']
coll = db.USPTO_coll

filepath = "C:\\Users\\zakaria\\Dowloads\\usptodata.csv"
df = pd.read_csv(filepath)

df=pd.read_csv(csv_path, error_bad_lines=False)
keyword = 'keyword'
df['keyword'] = pd.Series([keyword for x in range(len(df.index))])
print(df.head())
df.reset_index(drop=True,inplace=True)

data= df.to_dict('records')
#coll.remove({})
coll.insert_many(data)