

import pandas as pd
from bs4 import BeautifulSoup
import re as regex



class Parser():
    
    
    def __init__(self,json):
        
        self.json = json

    def single_page_parser(self):
        
        pass
    
    
    def single_element_parser(self,element):
        
        pass



class ParserSJS_ABlist(Parser):
    
    
    def __init__(self,json):
        
        super().__init__(json)
    

    
    
    def single_page_parser(self):
        
        bk_list = []
        industry_list = []
        a_name_list = []
        b_name_list = []
        a_ticker_list = []
        b_ticker_list = []
        link_list = []

        
        if len(self.json) == 4:
            
            stock_data = json[3]
            
            if stock_data["error"] is not None:
                
                print("Error")
                return None
                
            else:
                
                stock_data = stock_data["data"]
                
                for stock in stock_data:
                    
                    bk,industry,a_name,b_name,a_ticker,b_ticker,link = self.single_element_parser(stock)
                    
                    bk_list.append(bk)
                    a_name_list.append(a_name)
                    b_name_list.append(b_name)
                    a_ticker_list.append(a_ticker)
                    b_ticker_list.append(b_ticker)
                    industry_list.append(industry)
                    link_list.append(link)
        
        bk_list = pd.Series(bk_list)   
        a_name_list = pd.Series(a_name_list)   
        b_name_list = pd.Series(b_name_list)
        a_ticker_list = pd.Series(a_ticker_list)   
        b_ticker_list = pd.Series(b_ticker_list)   
        industry_list = pd.Series(industry_list)   
        link_list = pd.Series(link_list)  
        
        stock_df = pd.concat([bk_list,a_name_list,b_name_list,a_ticker_list,b_ticker_list,industry_list,link_list],axis=1)
        stock_df.columns = ["bk","a_name","b_name","a_ticker","b_ticker","industry","link"]
        
        return stock_df
                       
    
    
    def single_element_parser(self,stock):
        
        bk = stock["bk"]
        a_ticker = stock["agdm"]
        b_ticker = stock["bgdm"]
        industry = stock["sshymc"]
        
        link_name = stock["agjc"]
        soup = BeautifulSoup(link_name, 'html.parser')
        result = soup.find("a")
        
        link = result.get("href")
        a_name = result.string
        b_name = stock["bgjc"]
            
        
        return (bk,industry,a_name,b_name,a_ticker,b_ticker,link)




class ParserSJS_Alist(Parser):
    
    def __init__(self,json):
        
        super().__init__(json)
    
    
    
    def single_page_parser(self):
        
        bk_list = []
        industry_list = []
        name_list = []
        ticker_list = []
        gb_list = []
        ltgb_list = []
        link_list = []
        
        if len(self.json) == 4:
            
            stock_data = json[0]
            
            if stock_data["error"] is not None:
                
                print("Error")
                return None
                
            else:
                
                stock_data = stock_data["data"]
            
            for stock in stock_data:
                
                bk,industry,name,ticker,gb,ltgb,link = self.single_element_parser(stock)
                
                bk_list.append(bk)
                industry_list.append(industry)
                name_list.append(name)
                ticker_list.append(ticker)
                gb_list.append(gb)
                ltgb_list.append(ltgb)
                link_list.append(link)
                
        bk_list = pd.Series(bk_list) 
        industry_list = pd.Series(industry_list)   
        name_list = pd.Series(name_list)   
        ticker_list = pd.Series(ticker_list)   
        gb_list = pd.Series(gb_list)   
        ltgb_list = pd.Series(ltgb_list)
        link_list = pd.Series(link_list)  
        
        
        stock_df = pd.concat([bk_list,industry_list,name_list,ticker_list,gb_list,ltgb_list,link_list],axis=1)
        stock_df.columns = ["bk","industry","name","ticker","gb","ltgb","link"]
        return stock_df
        
    
    
    def single_element_parser(self,stock):
        
        bk = stock["bk"]
        ticker = stock["agdm"]
        gb = stock["agzgb"]
        ltgb = stock["agltgb"]
        industry = stock["sshymc"]
        
        link_name = BeautifulSoup(stock["agjc"],"html.parser")
        link = link_name.find("a").get("href")
        name = link_name.find("a").string
        
        
        
        return (bk,industry,name,ticker,gb,ltgb,link)




class ParserSJS_Blist(Parser):
    
    def __init__(self,json):
        
        super().__init__(json)
    
    
    
    def single_page_parser(self):
        
        bk_list = []
        industry_list = []
        name_list = []
        ticker_list = []
        gb_list = []
        ltgb_list = []
        link_list = []
        
        if len(self.json) == 4:
            
            stock_data = json[1]
            
            if stock_data["error"] is not None:
                
                print("Error")
                
                return None
                
            else:
                
                stock_data = stock_data["data"]
            
            for stock in stock_data:
                
                bk,industry,name,ticker,gb,ltgb,link = self.single_element_parser(stock)
                
                bk_list.append(bk)
                industry_list.append(industry)
                name_list.append(name)
                ticker_list.append(ticker)
                gb_list.append(gb)
                ltgb_list.append(ltgb)
                link_list.append(link)
                
        bk_list = pd.Series(bk_list) 
        industry_list = pd.Series(industry_list)   
        name_list = pd.Series(name_list)   
        ticker_list = pd.Series(ticker_list)   
        gb_list = pd.Series(gb_list)   
        ltgb_list = pd.Series(ltgb_list)
        link_list = pd.Series(link_list)  
        
        
        stock_df = pd.concat([bk_list,industry_list,name_list,ticker_list,gb_list,ltgb_list,link_list],axis=1)
        stock_df.columns = ["bk","industry","name","ticker","gb","ltgb","link"]
        return stock_df
        
    
    
    def single_element_parser(self,stock):
        
        bk = stock["bk"]
        ticker = stock["bgdm"]
        gb = stock["bgzgb"]
        ltgb = stock["bgltgb"]
        industry = stock["sshymc"]
        
        link_name = BeautifulSoup(stock["bgjc"],"html.parser")
        link = link_name.find("a").get("href")
        name = link_name.find("a").string
        
        
        return (bk,industry,name,ticker,gb,ltgb,link)






class ParserSJS_News(Parser):
    
    
    def __init__(self,text):
        
        html_file = BeautifulSoup(text,"html.parser")
        
        self.base = "http://www.szse.cn"
        
        super().__init__(html_file)
    
    
    
    def single_page_parser(self):
        
        time_list = []
        title_list = []
        link_list = []
        
        article_list = self.json.find("div",{"class":"article-list"})
        article_list = article_list.find("ul",{"class":"newslist date-right"})
        article_list = article_list.find_all("li")
        
        for article in article_list:
            
            time,title,link = self.single_element_parser(article)
            
            time_list.append(time)
            title_list.append(title)
            link_list.append(link)
        
        time_list = pd.Series(time_list)
        title_list = pd.Series(title_list)
        link_list = pd.Series(link_list)
        
        article_df = pd.concat([time_list,title_list,link_list],axis=1)
        
        return article_df
            
    
    def single_element_parser(self,article):
        
        article = article.find("div",{"class":"title"})
        script = article.find("script")
        
        match = regex.search(r"var curHref = '(.*?)';",str(script))
        link = match.group(1)
        link = self.base + link[1:]
        
        
        match = regex.search(r"var curTitle = '(.*?)';",str(script))
        title = match.group(1)
        
        time = article.find("span",{"class":"time"}).string.strip()
        
        return (time,title,link)
        


class ParserSJS_TP(ParserSJS_News):
    
    
    def __init__(self,text):
        
        
        super().__init__(text)

        self.base = "http://www.szse.cn/disclosure/notice/temp"
    
    


class ParserSJS_JG(ParserSJS_News):
    
    def __init__(self,text):
        
        super().__init__(text)
        
        self.base = "http://www.szse.cn/disclosure/supervision/dynamic"



class ParserSJS_XPKP(Parser):
        
    def __init__(self,json):
        
        super().__init__(json)
      
    def single_page_parser(self):
        
        ticker_list = []
        name_list = []
        rank_list = []
        year_list = []
        
        if len(self.json) == 3:
            
            info_data = self.json[2]
            
            if info_data["error"] is not None:
                
                print("Error")
                
                return None
            
            else:
                
                rank_data = info_data["data"]
                
                for stock in rank_data:
                    
                    year,ticker,name,rank = self.single_element_parser(stock)
                    
                    ticker_list.append(ticker)
                    name_list.append(name)
                    rank_list.append(rank)
                    year_list.append(year)
                    
            year_list = pd.Series(year_list)
            ticker_list = pd.Series(ticker_list)
            name_list = pd.Series(name_list)
            rank_list = pd.Series(rank_list)
            
            df = pd.concat([year_list,ticker_list,name_list,rank_list],axis=1)
                    
            return df                 
                
    
    def single_element_parser(self,stock):
        
        ticker = stock["gsdm"]
        name = stock["gsjc"]
        rank = stock["kpjg"]
        year = stock["kpnd"]
        
        return (year,ticker,name,rank)

