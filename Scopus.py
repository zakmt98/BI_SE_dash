def scopus(keywords,year):
    import time
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.utils import ChromeType
    from selenium.webdriver.common.by import By
    import pandas as pd
    from pymongo import MongoClient,TEXT
    from selenium.webdriver.chrome.options import Options
    import os
    import glob 
    
    begin=time.time()
    client = MongoClient('localhost', 27017)
    col= client['BI_PROJECTS_DB']
    db = col.Scopus
    db1=col.ScopusDataBase
    cur = db1.find()     
    results = list(cur)  

    if len(results)==0:
        print("Empty Cursor")
    
        browser = webdriver.Chrome(executable_path=ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
        def enable_download_headless(browser,download_dir):
            browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            browser.execute("send_command", params)
        download_dir = "C:\\Users\\Aymane Hasnaoui\\Desktop\\Scopus"
        enable_download_headless(browser, download_dir)
        browser.get("https://www.scopus.com/")
        browser.find_element_by_class_name("btn-text").click()
        browser.find_element_by_css_selector("#bdd-email").send_keys("aymane.hasnaoui1@gmail.com")
        browser.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()
        browser.find_element_by_css_selector("#bdd-password").send_keys("zbalboula")
        browser.find_element_by_css_selector("#bdd-elsPrimaryBtn").click()
        browser.find_element_by_css_selector("#bookTitle").click()
        time.sleep(80)
        browser.quit()
        os.chdir('C:\\Users\\Aymane Hasnaoui\\Desktop\\Scopus')
        extension = 'xlsx'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

        if len(all_filenames)!=0:

            for f in all_filenames:
                
                df = pd.DataFrame(pd.read_excel(f"C:\\Users\\Aymane Hasnaoui\\Desktop\\Scopus\\{f}"))
                df['keywords']=pd.Series([keywords for i in range(len(df.index))])
                df_dict=df.to_dict('records')
                df=df.fillna(value='None')
                db1.create_index([("Title",TEXT)])
                db1.insert_many(df_dict)
                
                
                os.path.basename(f"C:\\Users\\Aymane Hasnaoui\\Desktop\\springer\\{f}")
                os.remove(f) 
        else:
            print('file not found')
        
        
    else:
        print("pleine")
        
    a=db1.find({"$text":{"$search":f"\"{keywords}\""},"Publication year":year[0]})
    for i in a:
        db.insert_one(i)
    end=time.time()-begin
    print(end)
    return end
