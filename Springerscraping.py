
def springer(search):
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from itertools import zip_longest
    import csv
    import pymongo
    from pymongo import MongoClient

    client = MongoClient('localhost', 27017)
    db = client.BI_PROJECTS_DB.Springer
    
    def already_exist(db,search):
        if db.find({"keywords":search}).count() > 0:
            return False
        else:
            return True
       
    if(already_exist(db,search)):
        serielinks=[]
        #serietitles=[]
        #serieabstracts=[]
        #seriescategories=[]


        #journaltitles=[]
        #journalcategories=[]
        #journalauthors=[]
        #journalabstracts=[]

        #webcategory=[]
        #webtitle=[]

        #bookauthors=[]
        #booktitles=[]
        #bookcategories=[]
        #bookabstracts=[]
        #bookprices=[]
        booklinks=[]
        #isbnlists=[]

        #series=[]

        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        data=[]
        data1=[]
        browser.get("https://link.springer.com/")

        browser.find_element_by_css_selector("#query").send_keys(search)
        browser.find_element_by_css_selector("#search").click()
        browser.implicitly_wait(5)
        i=1
        try:
            while(browser.find_element_by_css_selector("#result-list") and (browser.find_element_by_xpath("//p[@class='result-count-message']/strong").text) != "0 results" and i==int(browser.find_element_by_css_selector(".page-number").get_attribute("value")) ):
                
                webpage=browser.find_elements_by_css_selector(".result-type-editorial")
                booklist=browser.find_elements_by_css_selector(".result-type-book")
                serielistt=browser.find_elements_by_css_selector(".result-type-series")
                journallist=browser.find_elements_by_css_selector(".result-type-journal")
                for book in booklist:    
                    book1={}

                    book1['category']=book.find_element_by_css_selector(".result-type").text.strip()
                    # bookcategory=book.find_element_by_css_selector(".result-type")
                    # bookcategories.append(bookcategory.text.strip())

                    book1['title']= book.find_element_by_css_selector("h4").text.strip()
                    # booktitl=book.find_element_by_css_selector("h4")
                    # booktitles.append(booktitl.text.strip())
                    
                    book1['authors']=book.find_element_by_css_selector(".book-contributors").text    
                    # bookauthor=book.find_element_by_css_selector(".book-contributors")
                    # bookauthors.append(bookauthor.text.strip())
                    
                    book1['abstracts']=book.find_element_by_css_selector(".snippet").text.strip()     
                    # bookabstract=book.find_element_by_css_selector(".snippet")
                    # bookabstracts.append(bookabstract.text.strip())

                    book1['price']=book.find_element_by_css_selector(".price").text.strip()
                    # bookprice=book.find_element_by_css_selector(".price")
                    # bookprices.append(bookprice.text.strip())

                    
                    booklink=book.find_element_by_css_selector("a").get_attribute('href')
                    book1["link"]=booklink
                    booklinks.append(booklink)

                    book1["keywords"]=search
                    data.append(book1)


                    for web in webpage:
                        web1={}
                        web1["category"]=web.find_element_by_css_selector(".result-type").text.strip()

                        #wcategorie=web.find_element_by_css_selector(".result-type")
                        #webcategory.append(wcategorie.text.strip())

                        web1["title"]=web.find_element_by_css_selector(".editorial").text
                        #webtitl=web.find_element_by_css_selector(".editorial")
                        #webtitle.append(webtitl.text.strip())
                        
                        web1["authors"]=None
                        web1["abstracts"]=None
                        web1["price"]=None
                        web1["link"]=web.find_element_by_css_selector("a").get_attribute('href')
                        web1["keywords"]=search
                        data.append(web1)



                    for serie in serielistt:
                        serie1={}

                        serie1["category"]=serie.find_element_by_css_selector(".result-type").text
                        #seriecategory=serie.find_element_by_css_selector(".result-type")
                        #seriescategories.append(seriecategory.text.strip())

                        serie1["title"]=serie.find_element_by_css_selector("h4").text
                        #serietitle=serie.find_element_by_css_selector("h4")
                        #serietitles.append(serietitle.text.strip())

                        serie1["authors"]=None
                        serie1["abstracts"]=None
                        serie1["price"]=None
        
                        serielink=serie.find_element_by_css_selector("a").get_attribute('href')
                        serie1["link"]=serielink
                        serielinks.append(serielink)
                        serie1["keywords"]=search

                        data.append(serie1)



                    for journal in journallist:    
                        journal1={}    
                
                        journal1["category"]=journal.find_element_by_css_selector(".result-type").text
                        #journalcategory=journal.find_element_by_css_selector(".result-type")
                        #ournalcategories.append(journalcategory.text.strip())

                        journal1["title"]=journal.find_element_by_css_selector("h4").text
                        #journaltitl=journal.find_element_by_css_selector("h4")
                        #journaltitles.append(journaltitl.text.strip())
                            
                        journal1["authors"]=journal.find_element_by_css_selector(".journal-contributors").text
                        #journalauthor=journal.find_element_by_css_selector(".journal-contributors")
                        #journalauthors.append(journalauthor.text.strip())
                    
                        journal1["abstracts"]=journal.find_element_by_css_selector(".snippet").text
                        #journalabstract=journal.find_element_by_css_selector(".snippet")
                        #journalabstracts.append(journalabstract.text.strip())

                        journal1["price"]=None
                        journal1["link"]=journal.find_element_by_css_selector("a").get_attribute('href')
                        journal1["keywords"]=search
                        data.append(journal1)
                browser.find_element_by_css_selector(".next").click()
                i+=1
        except:
            msg='no more data'
            print(msg)    

            
        for link in booklinks:
            book2={}
            browser.get(link)
            try:
                book2["links"]=link

                book2["isbn"]=browser.find_element_by_xpath("//dl/dd[@itemprop='isbn']").text

                book2["title"]=None
                book2["abstracts"]=None
                book2["keywords"]=search
                data1.append(book2)

                
            except:
                msg='no data'
                print(msg)
                

        for linkserie in serielinks:
            browser.get(linkserie)
            serie2={}
            try:
                serie2["link"]=linkserie
                serie2["isbn"]=None

                serie2['title']=browser.find_element_by_css_selector('h1').text
                #serietitles.append(serietitle)
            
                serie2["abstracts"]=browser.find_element_by_css_selector('p').text
                #serieabstracts.append(serieabstract.text.strip())
                
                serie2["keywords"]=search

                data1.append(serie2)
            except:
                msg="no serie data"
                print(msg)




        # webpagelist=[webcategory,webtitle]
        # webexported=zip_longest(* webpagelist)

        # booklists=[bookcategories,booktitles,bookauthors,bookabstracts,bookprices,booklinks,isbnlists]
        # bookexported=zip_longest(* booklists)

        # serielistss=[seriescategories,serietitles,[],serieabstracts,[],serielinks]
        # serieexported=zip_longest(* serielistss)

        # journallists=[journalcategories,journaltitles,journalauthors,journalabstracts,[],[]]
        # journalexported=zip_longest(* journallists)




        # with open("c:/Users/Aymane Hasnaoui/Desktop/test1.csv","w",encoding='utf-8') as myfile:
        #     wr=csv.writer(myfile)
        #     wr.writerow(["category","title","authors","abstract","prices"])
        #     wr.writerows(webexported)
        #     wr.writerows(bookexported)
        #     wr.writerows(journalexported)
        #     wr.writerows(serieexported)

        # data=[webexported,bookexported,journalexported,serieexported]
        def connect(db,col):
            client = pymongo.MongoClient('localhost:27017')
            db = client[db]
            dbcol=db[col]
            return dbcol

        def save(da,db,col):
            db=connect(db,col)
            try:
                db.insert_many(da)
                print(f'inserted {len(da)} object')
            except:
                print('an error occurred quotes were not stored to db')  

        print(data)        
        save(data,"BI_PROJECTS_DB","Springer")
        save(data1,"BI_PROJECTS_DB","SpringerDetails")
        browser.quit()
#springer("python")   