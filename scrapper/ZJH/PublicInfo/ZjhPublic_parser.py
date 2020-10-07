import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time


class Parser():
    
    
    def __init__(self,text):
        
        self.text = text

    def single_menu_page_parser(self):
        
        pass
    
    
    def single_element_parser(self,element):
        
        pass


class ParserZJH_PublicInfo(Parser):
    def __init__(self,text):
        '''year_list: a list of years we want to scrape
        '''
        soup = BeautifulSoup(text,"html.parser")
        
        super().__init__(soup)
    
        self.url = 'http://www.csrc.gov.cn/wcm/govsearch/year_gkml_list.jsp'

    def single_menu_page_parser(self):
        
        self.link_list = []
        for link in self.text.find_all('a')[1:]:
            self.link_list.append(link['href'])

        return self.link_list

    def single_element_parser(self,element):
        link = element
            
        #parse page info
            
        index = self.text.find_all('td')[0].find_all('td')[0].text.split(':')[1]
            

        category = self.text.find_all('td')[0].find_all('td')[1].text.replace('\n','')
        category = category.replace('\xa0','').split(':')[1]

        organization = self.text.find_all('td')[3].find_all('td')[0].text
        organization = organization.replace('\n','').split(':')[1]

        date = self.text.find_all('td')[3].find_all('td')[1].text
        date = date.replace('\n','').split(':')[1]

        name = self.text.find_all('td')[6].find('span').text

        file_num = self.text.find_all('td')[7].find_all('td')[0].text
        file_num = file_num.replace('\u3000','')
        file_num = file_num.replace('\n','').split(":")[1]

        theme = self.text.find_all('td')[7].find_all('td')[1].find('span').text

        try:
            content = self.text.find_all('div',{'class':"Custom_UnionStyle"})[0].get_text()
            content = content.replace('\n','')
            content = content.replace('\u3000','')
            content = content.replace('\xa0','')
            #no content case
        except IndexError:
            content = ''
    
        try:
            attached_file_url = self.text.find_all('div',{'class':'content'})[1].find('a')['href']
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
        
            
        return tempt_df
