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
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "<path_to_download_default_directory>",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
keywords = input('enter a keywords for searching:  ')
url = "https://worldwide.espacenet.com/patent/search?q=Keyword"
url = url.replace('Keyword', keywords)

browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

download_dir = 'C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\espacenet'

enable_download_headless(browser, download_dir)
browser.get(url)
time.sleep(5)
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "publications-list__wrapper--1Oeha-tH")))
browser.find_element_by_id('more-options-selector--publication-list-header').click()
time.sleep(5)
browser.find_element(By.XPATH,'//section[contains(@class,"prod-jss540") and .//text()="Download"]').click()


