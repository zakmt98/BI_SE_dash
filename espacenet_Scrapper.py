from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pprint
from pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost', 27017)
db = client['BI_project_db']
coll = db.espacenet_coll
def Espacenet_scrapper(keywords):
    begin=time.time()
    def enable_download_headless(browser, download_dir):
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        browser.execute("send_command", params)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })

    
    url = "https://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=singleline&query=Keyword"
    url = url.replace('Keyword', keywords)

    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

    download_dir = 'C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\espacenet'

    enable_download_headless(browser, download_dir)
    browser.get(url)
    time.sleep(5)
    button = browser.find_element(By.ID,'compactLink').click()
    time.sleep(1)
    button = browser.find_element(By.XPATH,'//*[@id="downloadCheck"]').click()
    time.sleep(3)
    button = browser.find_element(By.XPATH,'/html/body/div[1]/div[6]/div/div[2]/div[1]/ul/li[6]/a[2]').click()

    # time.sleep(8)
    # browser.get('chrome://downloads')
    # time.sleep(5)
    # filename = browser.execute_script(
    #     "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")

    # csv_path = "C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\espacenet\\"+filename
    # df=pd.read_csv(csv_path, error_bad_lines=False)
    
    # df['keyword'] = pd.Series([keywords for x in range(len(df.index))])
    # print(df.head())
    # df.reset_index(drop=True,inplace=True)

    # data= df.to_dict('records')
    # #coll.remove({})
    # coll.insert_many(data)
    #browser.get(url)
    #time.sleep(5) 
    i=0
    k=1
    while i==0:
    
        try:
            browser.find_element(By.ID,'nextPageLinkTop').click()
            time.sleep(3)
            #button = browser.find_element(By.ID,'compactLink').click()
            #time.sleep(3)
            button = browser.find_element(By.XPATH,'//*[@id="downloadCheck"]').click()
            time.sleep(3)
            button = browser.find_element(By.XPATH,'/html/body/div[1]/div[6]/div/div[2]/div[1]/ul/li[6]/a[2]').click()
            time.sleep(5)
            k+=1

        except:
            i=1
   
            
    filename = 'results.csv'
    for i in range(2,k+2):
        print(filename)
        csv_path = "C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\espacenet\\"+filename
        filename = 'results(page_'+str(i)+').csv'
        df=pd.read_csv(csv_path, error_bad_lines=False)
        
        df['keyword'] = pd.Series([keywords for x in range(len(df.index))])
        print(df.head())
        df.reset_index(drop=True,inplace=True)

        data= df.to_dict('records')
    # #coll.remove({})
        coll.insert_many(data)

    
    end=time.time()-begin
    return end
Espacenet_scrapper('scrapping data')