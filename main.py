from flask import Flask ,render_template,request
from flask_wtf import FlaskForm
from forms import BasicForm
from PubMed_Scrapper import scrapp_data
from IEEE_Scrapper import IEEE_scrapper
from USPTO_Scrapper import USPTO_Scrapper

app = Flask(__name__)
app.secret_key = '123'

@app.route('/',methods =['POST','GET'])
def main():

   return render_template("index.html")

@app.route('/Search',methods =['POST','GET'])
def search():
   
   if request.method== 'POST':

       keyword=request.form.get('keyword')
       #scrapp_data(keyword)
       for i in request.form.getlist('website'):
           print(type(i))
           if i=='1':
               scrapp_data(keyword)
           elif i=='2':
               IEEE_scrapper(keyword)
           elif i=='3':
               USPTO_Scrapper(keyword)
           elif i=='4':
               scrapp_data(keyword)


       return render_template("Search.html")
 

if __name__ == '__main__':
   app.run(debug = True)

