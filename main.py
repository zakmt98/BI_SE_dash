from flask import Flask ,render_template,request

from PubMed_Scrapper import scrapp_data
from IEEE_Scrapper import IEEE_scrapper
from USPTO_Scrapper import USPTO_Scrapper
from espacenet_Scrapper import Espacenet_scrapper
from springer import springer
from Scopus import scopus
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['BI_PROJECTS_DB']
coll = db.Ex_time_coll
coll1= db.History

year=[]

app = Flask(__name__)
app.secret_key = '123'

@app.route('/',methods =['POST','GET'])
def main():

   return render_template("index.html")

@app.route('/Search',methods =['POST','GET'])
def search():
   
   if request.method== 'POST':
       for i in request.form.getlist('year'):
           #print(type(i))
           if i=='1':
               year.append("2017")
           elif i=='2':
               year.append("2018")
           elif i=='3':
               year.append("2019")
           elif i=='4':
               year.append("2020")
           elif i=='5':
               year.append("2021")
       
       keyword=request.form.get('keyword')
       #scrapp_data(keyword)
       ex_times={}
       for i in request.form.getlist('website'):
           print(type(i))
           if i=='1':
              ex_time = Espacenet_scrapper(keyword)
              ex_times["Espacenet_scrapper"] = ex_time

           elif i=='2':
               ex_time=scopus(keyword,year)
               ex_times["scopus"] = ex_time
               coll1.insert_one({"website":"Scopus","keyword":keyword,"year":year})
           elif i=='3':
               ex_time=USPTO_Scrapper(keyword)
               ex_times["USPTO_Scrapper"] = ex_time
           elif i=='4':
               ex_time=springer(keyword,year)
               ex_times["springer"] = ex_time
               coll1.insert_one({"website":"Springer","keyword":keyword,"year":year}) 
               
           elif i=='5':
               ex_time=scrapp_data(keyword)
               ex_times["PubMed-Scrapper"] = ex_time
           elif i=='6':
               ex_time=IEEE_scrapper(keyword)
               ex_times["IEEE_scrapper"] = ex_time
       coll.insert_one(ex_times)


       return render_template("index.html")
 

if __name__ == '__main__':
   app.run(debug = True)

