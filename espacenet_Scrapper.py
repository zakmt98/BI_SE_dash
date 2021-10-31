from itertools import zip_longest
import csv
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re
import pymongo
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from shutil import copyfile
import splinter
from selenium.webdriver.chrome.options import Options
import os
import glob
import pandas as pd





def DataBase():
    print('drel l toDB')
    filepath = 'C:\\Users\\hixam\\Desktop\\scraped\\combined_csv.csv' 
    import_content(filepath)


def to_CSV():

    os.chdir('C:\\Users\\hixam\\Desktop\\scraped')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    for f in all_filenames:
        os.remove(f) 
    #export to csv
    # path='C:\\Users\\hixam\\Desktop\\scraped'
    combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')

    donewell()
def donewell():
    print('csv combined WELL !1!2!3')

    
def import_content(filepath):
    mng_client = pymongo.MongoClient('localhost:27017')
    mng_db = mng_client['BI_PROJECTS_DB']
    collection_name = 'ESPACENET' 
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)
    print('doneeeeeeeee!!!!!!!!!!!!!!!!!!!!!!')
    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)
    print('csv saved WELL !!!')

key=str(input('what is your keys word :  '))
search=re.sub(" ","+",key)
# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)
chrome_options = Options()

chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = "C:\\Users\\hixam\\Desktop\\scraped"
enable_download_headless(browser, download_dir)

url=f'https://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=singleline&query={search} '
browser.get(url)

nextPage=True
i=1
while(nextPage and i<5):
    print(str(i)+' rani d5olt')
    time.sleep(3)

    #CSV file 
    csvFile=browser.find_element_by_css_selector('a.exportLink')
    if(csvFile):
        csvFile.click()
        time.sleep(1)
        print('csv file downoalded well !!')
    else :
        print('page'+str(i)+'  csv file not found !!')

    # nextPage=False

    try:
        next_page=element=browser.find_element(By.ID,"nextPageLinkTop")
        if(next_page):
            next_page.click();
            nextPage=True
            i+=1
    except:
            print('all pages were scriped!!')
            nextPage=False
            time.sleep(1)

browser.quit()        


to_CSV()
time.sleep(3)
data=pd.read_csv('C:\\Users\\hixam\\Desktop\\scraped\\combined_csv.csv')
for i in range(0,len(data)):
    data['keyWord']=key
data.to_csv("C:\\Users\\hixam\\Desktop\\scraped\\combined_csv.csv", index=False)
DataBase()
print('daaaaaaaaaaaaaaaz')
