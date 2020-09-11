import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

class ZhengjianhuiPublic():
    def __init__(self,year_list):
        '''year_list: a list of years we want to scrape
        '''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'}
    
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
        soup = BeautifulSoup(response.content,'html.parser')
        for link in soup.find_all('a')[1:]:
            self.link_list.append(link['href'])
    
    def start_requests_one_year_rest_of_page(self,year):
        page_num = 2
        while True:
            print("Start scraping page {0} in {1}".format(page_num,str(year)))
            form = {'page':page_num,
                     'schn':'832',
                     'sinfo':'',
                     'years':str(year),
                     'countpos':'0',
                     'curpos':'主题分类'
            }
            response = requests.post(self.url,form)
            soup = BeautifulSoup(response.content,'html.parser')
            tempt_link_list = soup.find_all('a')[1:]
            if len(tempt_link_list)>0:
                #loop in each page's link
                for link in tempt_link_list:
                    self.link_list.append(link['href'])
                page_num += 1
            # check if current page exceeds max page
            else:
                break
    
    def start_requests_all_years(self):
        for year in self.year_list:
            print(year)
            self.start_requests_one_year_first_page(year)
            self.start_requests_one_year_rest_of_page(year)
        self.link_list = ['http://www.csrc.gov.cn'+link for link in self.link_list]
    
    def store_link_all_years(self):
        self.start_requests_all_years()
        link_df = pd.DataFrame(self.link_list,columns = ['link'])
        year_name_list = [str(year) for year in self.year_list]
        link_df.to_csv('_'.join(year_name_list)+".csv",index = False)
        return link_df
    
    def parse_pages(self):
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
            
            soup = BeautifulSoup(response.content,'html.parser')
            
            #parse page info
            
            index = soup.find_all('td')[0].find_all('td')[0].text.split(':')[1]
            

            category = soup.find_all('td')[0].find_all('td')[1].text.replace('\n','')
            category = category.replace('\xa0','').split(':')[1]

            organization = soup.find_all('td')[3].find_all('td')[0].text
            organization = organization.replace('\n','').split(':')[1]

            date = soup.find_all('td')[3].find_all('td')[1].text
            date = date.replace('\n','').split(':')[1]

            name = soup.find_all('td')[6].find('span').text

            file_num = soup.find_all('td')[7].find_all('td')[0].text
            file_num = file_num.replace('\u3000','')
            file_num = file_num.replace('\n','').split(":")[1]

            theme = soup.find_all('td')[7].find_all('td')[1].find('span').text

            try:
                content = soup.find_all('div',{'class':"Custom_UnionStyle"})[0].get_text()
                content = content.replace('\n','')
                content = content.replace('\u3000','')
                content = content.replace('\xa0','')
            #no content case
            except IndexError:
                content = ''
    
            try:
                attached_file_url = soup.find_all('div',{'class':'content'})[1].find('a')['href']
                attached_file_url = attached_file_url[1:]
                prefix = re.compile('(.+)/t20')
                prefix = prefix.search(link).group(1)
                attached_file_url = prefix +attached_file_url
            except (TypeError,IndexError):
                attached_file_url = ''
                
            #store in dictionary
            tempt_dict = {}
            tempt_dict['link'] = link
            tempt_dict['index'] = index
            tempt_dict['category'] = category
            tempt_dict['issued_organization'] = organization
            tempt_dict['issued_date'] = date
            tempt_dict['title'] = name
            tempt_dict['file_num'] = file_num
            tempt_dict['theme'] = theme
            tempt_dict['content'] = content
            tempt_dict['attached_file_url'] = attached_file_url
            tempt_df = pd.DataFrame(tempt_dict,index = [0])
            self.df_list.append(tempt_df)
            i = i+1
            
        #after get information for each link
        final_df = pd.concat(self.df_list)
        year_name_list = [str(year) for year in self.year_list]
        final_df.to_excel('_'.join(year_name_list)+"_all_info.xlsx",index = False)
        print('Finished scrapping')
        return final_df

if __name__ == "__main__":
    def main(year_list):
        scrapper = ZhengjianhuiPublic(year_list)
        scrapper.start_requests_all_years()
        final_df = scrapper.parse_pages()
        return final_df

    main([2020])