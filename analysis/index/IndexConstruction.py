
import pandas as pd
import jieba
from collections import Counter



class IndexConstruction():

    """
    This class is used to construct index by counting the number/ratio of occurance
    of a specific list of words. The index is similar to the EPU index introduced in
    Baker et al (2013).

    """
    
    def __init__(self,dictionary_directory,content_series):

        """
        The initialization requires a dictionary and a series of text.

        :param dictionary_directory: str
        :param content_series: pd.Series(str)

        """
        
        self.dictionary = self.__load_dictionary(dictionary_directory)
        self.content = content_series
        self.agg_content = None

    
    def __load_dictionary(self,dictionary_directory):

        """
        This function is used to load the dictionary from the directory.

        :param dictionary_directory: str

        :return: list(str)

        """
        
        with open(dictionary_directory) as f:
            
            dictionary = f.readlines()
            dictionary = [word.strip() for word in dictionary]
        
        return dictionary
    
    
    def _count_occurrance(self,text,cut_all=True,use_paddle=True):
        """
        This function counts the number of occurrance of the words in the dictionary
        in a single text.
        It cuts the text using jieba library. Then it counts the occurance and normailize it.

        :param text: str
        :param cut_all: boolean
        :param use_paddle: boolean

        :return: float

        """
        
        word_cut = list(jieba.cut(text,cut_all=cut_all,use_paddle=use_paddle))
        
        counter = Counter(word_cut)
        
        occ_agg = 0
        
        for word in self.dictionary:
            
            occ_agg += counter[word]
        
        if len(word_cut) == 0:
            
            return 0
        
        ratio  = occ_agg/len(word_cut) * 100
        
        return ratio
    
        
    def aggregate_content(self,freq):
        """
        This function aggregates the content series to certain frequency.
        This function is used to aggregate multiple policy/news based on the publishing date.
        It could aggregate based on daily, weekly or monthly frequency.


        :param freq: str (e.g. "B","W","BM")
        
        :return: pd.Series(str)

        """
        
        def func(x):
            
            total_string = ""
            
            try:
                for string in x:
                    
                    if not isinstance(string,str):
                        continue
                    
                    total_string += string
            except:
                
                print("Error.")
            
            return total_string
        
        aggregate_series = self.content.resample(freq,label="right",closed="right").apply(func)


        self.agg_content = aggregate_series
        
        return aggregate_series
    

    
    def calculate_score(self):
        """
        This function calculates the score of each content in the series of content.
        The score is based on counting the number of occurance of the words in the dict_list.


        :return: pd.Series(float)

        """
        
        def func(x):
            
            try:
                score = self._count_occurrance(x)
            except:
                score = 100

            return score
        
        score_list = self.agg_content.apply(func)
        
        return score_list
    






