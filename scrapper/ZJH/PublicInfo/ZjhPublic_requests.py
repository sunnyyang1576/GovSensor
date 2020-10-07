import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from ZjhPublic_parser import ParserZJH_PublicInfo

class Requests():
    
    
    def __init__(self):
        

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'}

    def menu_page_request(self):
        
        pass
    
    
    def element_request(self,element):
        
        pass



class RequestsZJH_PublicInfo(Requests):
    def __init__(self,year_list):
        '''year_list: a list of years we want to scrape
        '''
        super().__init__()
    
        self.url = 'http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp'
        self.year_list = year_list
        self.link_list = []

    def start_requests_one_year_first_page(self,year):
        print("Start scraping page 1 in {0}".format(str(year)))
        ##requests for first page
        form = {
       'schn':'832',
       'sinfo':'',
       'years':str(year),
       'countpos':'0',
       'curpos':'主题分类'}
        
        response = requests.post(self.url,form)
        return response
        
    
    def start_requests_one_year_rest_of_page(self,year):
        page_num = 2
        while True:
            try:
                print("Start scraping page {0} in {1}".format(page_num,str(year)))
                form = {'page':page_num,
                     'schn':'832',
                     'sinfo':'',
                     'years':str(year),
                     'countpos':'0',
                     'curpos':'主题分类'
                }
                response = requests.post(self.url,form)
                meau_parser = ParserZJH_PublicInfo(response.content)
                tempt_link_list = meau_parser.single_menu_page_parser()
                
                
                if len(tempt_link_list)>0:
                    for link in tempt_link_list:
                        self.link_list.append(link)
                    page_num += 1
                else:
                    break
            # check if current page exceeds max page
            except Error as e:
                break
        return self.link_list
    
    def menu_page_request(self):
        for year in self.year_list:
            print(year)
            self.start_requests_one_year_first_page(year)
            self.start_requests_one_year_rest_of_page(year)
        self.link_list = ['http://www.csrc.gov.cn'+link for link in self.link_list]
        return self.link_list
    
    
    def element_request(self):
        '''return a dataframe'''
        
        self.df_list = []
        ##loop in each link
        i = 0
        #get first 400 link
        #sub test 
        #for link in self.link_list[0:400]:
        for link in self.link_list:
            print('start parsing link '+ str(i))
            
            #if ip has been restricted,wait
            response = requests.get(link)
            while response.status_code == 404:
                time.sleep(30)
                response = requests.get(link)
            
            element_parser = ParserZJH_PublicInfo(response.content)
            tempt_df = element_parser.single_element_parser(link)
            #print(tempt_df)
            self.df_list.append(tempt_df)

            i = i+1
            
            
            #parse page info
            
        #after get information for each link
        final_df = pd.concat(self.df_list)
        final_df.reset_index(drop = True, inplace = True)
        print('Finished scrapping')
        return final_df


def main():
	ZJH_spider = RequestsZJH_PublicInfo([2020])
	ZJH_spider.menu_page_request()
	final_df = ZJH_spider.element_request()
	final_df.to_excel('sample.xlsx',index = False)


if __name__ == "__main__":
	main()

