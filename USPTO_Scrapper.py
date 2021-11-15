import pandas as pd
from pymongo import MongoClient



client = MongoClient('localhost', 27017)
db = client['BI_project_db']
coll = db.USPTO_coll
def insert_todata():
    filepath = "C:\\Users\\zakaria\\Downloads\\usptodata.csv"


    df=pd.read_csv(filepath, error_bad_lines=False)
    keyword = 'keyword'
    
    print(df.head())
    df.reset_index(drop=True,inplace=True)

    data= df.to_dict('records')
    #coll.remove({})
    coll.insert_many(data)
def USPTO_Scrapper(keyword):
    return 0

