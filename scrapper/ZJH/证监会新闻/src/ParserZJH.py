

import pandas as pd
from bs4 import BeautifulSoup
import re as regex
from bs4 import Tag, NavigableString, BeautifulSoup




class Parser():
    
    
    def __init__(self,text):
        
        self.text = text

    def single_menu_page_parser(self):
        
        pass
    
    
    def single_element_parser(self,element):
        
        pass



class ParserZJH(Parser):

    def __init__(self,text):
        
        html_file = BeautifulSoup(text,"html.parser")
        
        super().__init__(html_file)
        
        self.base = "http://www.csrc.gov.cn/pub/newsite"
    
    
    def single_menu_page_parser(self):
        
        time_list = []
        title_list = []
        link_list = []
        
        document_list = self.text.find("div",{"class":"fl_list"})
        document_list = document_list.find_all("li")
        
        for document in document_list:
            
            time,title,link = self.single_element_parser(document)
            
            time_list.append(time)
            title_list.append(title)
            link_list.append(link)
        
        time_list = pd.Series(time_list)
        title_list = pd.Series(title_list)
        link_list = pd.Series(link_list)
        
        df = pd.concat([time_list,title_list,link_list],axis=1)
        
        return df
    
    
    def single_element_parser(self,document):
        
        a = document.find("a")
        
        link = a.get("href")

        link = self.base + link[1:]
        
        title = a.string
        
        time = document.span.string
        
        return (time,title,link)
    
    
    def single_content_page_parser(self,text,parser="html5lib"):


        html_file = BeautifulSoup(text,parser)
        content = html_file.find("div",{"class":"content"})



        sub_content_list = content.children

        sub_sub_content_list = []

        for sub_content in sub_content_list:

            if isinstance(sub_content,NavigableString):
                sub_sub_content_list.append(sub_content)
                continue

            if isinstance(sub_content,Tag):

                if sub_content.name in ["style","script"]:
                    continue

                sub_sub_content_list+= list(sub_content.children)


        filter_sub_sub_content_list = []

        for sub_content in sub_sub_content_list:

            if sub_content.name in ["style","script"]:
                continue

            if sub_content == "\n":
                continue

            filter_sub_sub_content_list.append(sub_content)


        final_list = []

        for sub_content in filter_sub_sub_content_list:

            if isinstance(sub_content,NavigableString):
                final_list.append(sub_content)
                continue

            descendants_list = sub_content.descendants
            descendants_list = [descendant for descendant in descendants_list if isinstance(descendant,NavigableString)]
            final_list+=descendants_list

        total_string = "".join([string.strip() for string in final_list if string is not None])

        return total_string




class ParserZJH_ZJHYW(ParserZJH):

    def __init__(self,text):
        
        super().__init__(text)
        
        self.base = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd"
     



class ParserZJH_XWFBH(ParserZJH):
    
    def __init__(self,text):
        
        super().__init__(text)
        
        self.base = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwfbh"
    



class ParserZJH_ZCJD(ParserZJH):
    
    def __init__(self,text):
        
        super().__init__(text)
        
        self.base = "http://www.csrc.gov.cn/pub/newsite"
    
    
    def single_element_parser(self,document):
        
        a = document.find("a")
        
        link = a.get("href")
        
        link = self.base + link[5:]
        
        title = a.string
        
        time = document.span.string
        
        return (time,title,link)
    

