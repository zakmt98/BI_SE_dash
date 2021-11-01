from pandas.core.indexes.base import Index


def scopus(keywords):
    import time
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.utils import ChromeType
    from selenium.webdriver.common.by import By
    import pandas as pd
    from pymongo import MongoClient
    from selenium.webdriver.chrome.options import Options
    begin=time.time()
    client = MongoClient('localhost', 27017)
    db = client.BI_PROJECTS_DB.Scopus
    db1 =client.BI_PROJECTS_DB.timeofexecution
    def already_exist(db,search):
        if db.find({"keywords":search}).count() > 0:
            return False
        else:
            return True
       
    if(already_exist(db,keywords)):
    
        browser = webdriver.Chrome(executable_path=ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
    
        browser.get("https://www.scopus.com/")
        browser.find_element_by_class_name("btn-text").click()
        browser.find_element_by_css_selector("#bdd-email").send_keys("aymane.hasnaoui1@gmail.com")
        browser.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()
        browser.find_element_by_css_selector("#bdd-password").send_keys("zbalboula")
        browser.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()
        browser.find_element_by_css_selector("#gh-Sources").click()
        browser.implicitly_wait(5)
        browser.find_element_by_css_selector(".ui-selectmenu-text").click()
        browser.find_element_by_css_selector("#ui-id-2").click()

        browser.find_element_by_css_selector("#search-term").send_keys(keywords)

        browser.find_element_by_css_selector("#searchTermsSubmit").click()
        browser.implicitly_wait(5)
        NoA=browser.find_element(By.ID,"resultCount").text.replace(" results","")
        NoA=int(NoA)
        browser.implicitly_wait(10)
        browser.find_element(By.ID,"showAllPageBubble").click()
        browser.implicitly_wait(300)
        browser.find_element(By.XPATH,"//ul[@class='list-unstyled']/li").click()
        browser.find_element(By.ID,"exportText").click()
        time.sleep(8)
        if(NoA>1000):
            NoA=1000
        df = pd.DataFrame(pd.read_excel(f"C:/Users/Aymane Hasnaoui/Downloads/{NoA}-source-results.xlsx"))
        df['keywords']=pd.Series([keywords for i in range(len(df.index))])
        df=df.fillna(value='None')

        df_dict=df.to_dict('records')

        db.insert_many(df_dict)

        
        browser.quit()

    end=time.time()-begin
    return end