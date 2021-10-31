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

keywords = input('enter a keywords for searching:  ')
url = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=Keyword"
url = url.replace('Keyword', keywords)

browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
