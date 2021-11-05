from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


from pymongo import MongoClient




def get_PMID_file(keyword):
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

    keyword = keyword.replace(" ", "+")
    url = "https://pubmed.ncbi.nlm.nih.gov/?term=Keyword"
    url = url.replace('Keyword', keyword)

    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
    download_dir = 'C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\PubMed'

    enable_download_headless(browser, download_dir)
    browser.get(url)
    time.sleep(2)
    duration = browser.find_element(By.ID,'id_filter_datesearch.y_5').click()
    time.sleep(2)
    save = browser.find_element(By.ID,'save-results-panel-trigger').click()
    time.sleep(1)
    select = browser.find_element(By.ID,'save-action-selection').click()
    time.sleep(1)
    select = browser.find_element(By.XPATH,'/html/body/main/div[1]/div/form/div[1]/div[1]/select/option[2]').click()
    time.sleep(1)
    select = browser.find_element(By.ID, 'save-action-format').click()
    time.sleep(1)
    select = browser.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div[2]/select/option[3]').click()
    time.sleep(1)
    select = browser.find_element(By.CLASS_NAME,'action-panel-submit').click()

    browser.get('chrome://downloads')
    time.sleep(2)
    filename = browser.execute_script(
        "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
    time.sleep(2)
    file_path =  "C:\\Users\\zakaria\\PycharmProjects\\BI_project\\dataset\\PubMed\\"+filename
    file = open(file_path,'r')
    idlist = []
    for line in file:
        line = line.replace("\n", "")
        idlist.append(line)
    return idlist


def scrapp_data(keyword):
    begin=time.time()
    client = MongoClient('localhost', 27017)
    db = client['BI_project_db']
    coll = db.PubMed_db

    #keyword = str(input('Please enter the keyword '))
    #num = int(input('Please enter the number of results '))

    idlist = get_PMID_file(keyword)
    print(idlist)
    Articles = []
    for link in idlist:
        if already_exist(db,link):
            print("exist")
            continue
        else:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=idlist"
            url = url.replace("idlist", link)
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')

            # pprint.pprint(soup)

            row = get_info(soup,keyword)
            #Articles.append(row)
            #print(row)
            coll.insert_one(row)
       
    if len(Articles) != 0:
       """  coll.insert_many(Articles)
        print(Articles) """
    endprocess=time.time()-begin
    return endprocess


def get_info(soup,keyword):
    article_info = {}
    journal=soup.find('journal')
    #print(journal)
    try:
        articleTitle= soup.find('articletitle').text
    except:
        articleTitle='none'
    #print(date)

    #print(articleTitle)
    try:
        journalTitle = journal.find('title').text
        volume = journal.find('volume').text
    except:
        journalTitle = 'none'
        volume = 'none'

    try:
        issue = journal.find('issue').text
        date = journal.find('year').text + " " + journal.find('month').text
        abst = soup.select('AbstractText')[0].text
    except:
        issue = 'none'
        date = 'none'
        abst = 'none'

    #print(abst)
    authorlist = soup.find('authorlist')
    authors=""
    try : 
        for auth in authorlist.find_all('author'):
            try:
                lastname = auth.find('lastname').text
                initial = auth.find('initials').text
                author = ",".join([lastname, initial])

            except: 
                author = ""
            authors = author + " " + authors
    except:
        authors='none'

    #print(authors)
    try:
        country = soup.find('country').text
        language = soup.find('language').text
    except:
        country = 'none'
        language='none'
    pmid=soup.find('pmid').text
    PMarticleLink = "https://pubmed.ncbi.nlm.nih.gov/"+pmid
    #print(PMarticleLink)
    req = requests.get(PMarticleLink)
    #print(req)
    soup_article = BeautifulSoup(req.content, 'html.parser')
    link_list= soup_article.select('.full-text-links-list')
    links=[]
    for link in link_list:
        links.append(link.find('a')['href'])
    MH_list=[]
    try:
        for mh in soup.find('MeshHeadingList'):
            try:
                desc_name = mh.find('DescriptorName').text
            except:
                desc_name='none'
            MH_list.append(desc_name)
    except:
        MH_list = 'none'

    journal_info = ''
    info=soup.find('MedlineJournalInfo')
    try:
        journal_info =info.find('Country').text + '-'+info.find('MedlineTA').text + '-'+info.find('NlmUniqueID').text
    except:
        journal_info='none'

    article_info['pmid']=pmid
    article_info['articleTitle']=articleTitle
    article_info['date']=date
    article_info['journalTitle']=journalTitle
    article_info['journal_info'] = journal_info
    article_info['volume']= volume
    article_info['issue']=issue
    article_info['authors']= authors
    article_info['language'] = language
    article_info['country'] = country
    article_info['abstract'] = abst
    article_info['MeshHeading'] = MH_list
    article_info['links'] = links
    article_info['keyword'] = keyword
    return article_info

def already_exist(db,pmid):
    if db.PubMed_db.find({"pmid":pmid}).count() > 0:
        return True
    else:
        return False

scrapp_data('data')






