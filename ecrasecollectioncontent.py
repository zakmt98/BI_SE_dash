
import pymongo
client = pymongo.MongoClient('localhost:27017')
db= client.BI_PROJECTS_DB.Springer
db1= client.BI_PROJECTS_DB.ScopusDataBase
db2=client.BI_PROJECTS_DB.Scopus
db3=client.BI_PROJECTS_DB.Ex_time_coll
db4=client.BI_PROJECTS_DB.History

db.delete_many({})
db1.delete_many({}) 
db2.delete_many({})
db3.delete_many({})
db4.delete_many({})


