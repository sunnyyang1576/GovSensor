import re
import jieba



class Preprocess():
	"""
	This class is used to conduct basic preprocess on a single string.
	The basic process includes
	1. remove stopwords
	2. remove url
	3. remove digits
	4. cut the sentences into words

	"""
    
    
    def __init__(self,text):
    	"""
    	The initialization requires a single string.
    	It has three attributes
    	1. ori_text : the original text 
    	2. word_list : the list of words after the cut function
    	3. updated_text : the text after each step of preprocessing

    	:param text: str

    	"""
        
        self.ori_text = text
        self.word_list = []
        self.updated_text = text
        self.update = True
    
    def _import_stopwords_dict(self,dictionary_directory):
    	"""
    	This function is used to import the stopwords dictionary.
    	It has a default stopwords dictionary, but it also allows 
    	user-defined dictionary.

    	The dictionary should be a txt file in which each row is
    	a stopword.

    	:param dictionary_directory: str, a directory that represents a txt file

    	"""
        
        pass
    
    def cut_sentence(self):
    	"""
    	This function is used to cut the text into a list of words.
    	It currently relies on the jieba library.


    	"""
        
        pass
    
    def remove_digits(self):
    	"""
    	This function is used to remove the digits from the text.


    	"""
        
        punc = u'0123456789.'
        output_str = re.sub(r'[{}]+'.format(punc), '', self.updated_text)
        self.updated_text = output_str
        
    
    def remove_url(self):
    	"""
    	This function is used to remove the url from the text.


    	"""
        
        pattern = r'^https?:\/\/.*[\r\n]*'
        output_str = re.sub(pattern, '', self.updated_text, flags=re.MULTILINE)
        self.updated_text = output_str

    
    def remove_stop_words(self):
    	"""
    	This function is used to remove the stopwords from the text.

    	"""

              
        pass











