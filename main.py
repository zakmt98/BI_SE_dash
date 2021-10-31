from flask import Flask ,render_template,request
from flask_wtf import FlaskForm
from forms import BasicForm
from PubMed_Scrapper import scrapp_data
app = Flask(__name__)
app.secret_key = '123'

@app.route('/',methods =['POST','GET'])
def main():

   return render_template("index.html")

@app.route('/Search',methods =['POST','GET'])
def search():
   
   if request.method== 'POST':

       keyword=request.form.get('keyword')
       scrapp_data(keyword)
       print(request.form.getlist('Springer'))
       return render_template("Search.html")
 

if __name__ == '__main__':
   app.run(debug = True)

