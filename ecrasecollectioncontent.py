
import pymongo
client = pymongo.MongoClient('localhost:27017')
db= client.BI_PROJECTS_DB.Springer
db1= client.BI_PROJECTS_DB.SpringerDetails
db2=client.BI_PROJECTS_DB.Scopus
db3=client.BI_PROJECTS_DB.timeofexecution
db.delete_many({})
db1.delete_many({}) 
db2.delete_many({})
db3.delete_many({})


