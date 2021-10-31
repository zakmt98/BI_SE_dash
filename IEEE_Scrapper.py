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
coll = db.IEEE_col
def IEEE_scrapper(keywords):
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

    
    url = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=Keyword"
    url = url.replace('Keyword', keywords)

    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

    download_dir = 'C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\IEEE'

    enable_download_headless(browser, download_dir)
    browser.get(url)

    timeout = 30
    elem = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "List-results")))
    time.sleep(5)
    list = browser.find_element_by_class_name('global-content-width-w-rr-lr')
    # sublist=list.find_element_by_class_name('List-results-items')
    butan = browser.find_element_by_class_name('export-filter').click()
    time.sleep(2)
    download = browser.find_element_by_class_name('stats-SearchResults_Download').click()
    time.sleep(60)
    browser.get('chrome://downloads')
    time.sleep(5)
    filename = browser.execute_script(
        "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")


csv_path = "C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\IEEE\\"+"export2021.10.21-08.00.07.csv"
df=pd.read_csv(csv_path, error_bad_lines=False)
keyword = 'keyword'
df['keyword'] = pd.Series([keyword for x in range(len(df.index))])
print(df.head())
df.reset_index(drop=True,inplace=True)

data= df.to_dict('records')
#coll.remove({})
coll.insert_many(data)