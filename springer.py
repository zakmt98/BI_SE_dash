def springer(keywords):

    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from pymongo import MongoClient
    import time
    from selenium.webdriver.support.ui import Select
    import os
    import glob
    import pandas as pd

    begin=time.time()
    client = MongoClient('localhost', 27017)
    col = client['BI_project_db']
    db = col.springer

    
    def already_exist(db,search):
        if db.find({"keywords":search}).count() > 0:
            return False
        else:
            return True
       
    if(already_exist(db,keywords)):

        sy=2015
        ey=2017
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        def enable_download_headless(browser,download_dir):
            browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            browser.execute("send_command", params)
        download_dir = "C:\\Users\\zakaria\\Desktop\\springer"
        enable_download_headless(browser, download_dir)


        browser.get("https://link.springer.com/")
        browser.find_element_by_css_selector("#query").send_keys(keywords)
        browser.find_element_by_css_selector("#search").click()
        browser.implicitly_wait(5)
        #time.sleep(5)
        try:
            browser.find_element_by_css_selector("#onetrust-accept-btn-handler").click()
        except:
            msg="no"
        
        
        for i in range(sy,ey):
            browser.find_element_by_css_selector(".expander-title").click()
            try:
                browser.find_element_by_css_selector("#onetrust-accept-btn-handler").click()
            except:
                msg="no"
            select = Select(browser.find_element_by_id('date-facet-mode'))
            select.select_by_value('in')
            #time.sleep(3)

        
            browser.find_element_by_css_selector("#start-year").clear()
            #time.sleep()
            browser.find_element_by_css_selector("#start-year").send_keys(i)
            #time.sleep(5)
            browser.find_element_by_css_selector("#date-facet-submit").click()
            #time.sleep(3)
            browser.find_element_by_css_selector("#tool-download").click()
            browser.find_element_by_css_selector(".remove-hover").click()
            #time.sleep()
            
            df = pd.DataFrame(pd.read_csv("C:\\Users\\zakaria\\Desktop\\springer\\SearchResults.csv"))
            df['keywords']=pd.Series([keywords for i in range(len(df.index))])
            df_dict=df.to_dict('records')
            db.insert_many(df_dict)

            df.shape
            os.chdir('C:\\Users\\zakaria\\Desktop\\springer')
            extension = 'csv'
            all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
            # print(len(all_filenames))
            if len(all_filenames)!=0:
                for f in all_filenames:
                    filename = os.path.basename(f"C:\\Users\\zakaria\\Desktop\\springer\\{f}")
                    os.remove(f) 
            else:
                print('file not found')
        browser.quit()
    
    endprocess=time.time()-begin
    
    return endprocess
    
       
        
