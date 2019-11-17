#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#We create our preprocessing function

def preprocess(string):
    
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize
    
    #Remove punctuation and lower all characters
    words = nltk.word_tokenize(string)
    words = [word.lower() for word in words if word.isalnum()]
    
    #Remove stop words
    stop_words = set(stopwords.words('english'))
    words2 = [i for i in words if not i in stop_words]
    
    #Stemming
    stemmer= PorterStemmer()
    final = [stemmer.stem(word) for word in words2]
    
    return final


# In[ ]:


def load_files():
        
    # we load our simple index
    with open('simple_index.json') as json_file:
        simple_index = json.load(json_file)

    # we load our count index
    with open('count_index.json') as json_file:
        count_index = json.load(json_file)
        
    # we load our doc_count_words dictonary
    with open('doc_count_words.json') as json_file:
        doc_count_words = json.load(json_file)
    
    # we load our inverted_index
    with open('inverted_index.json') as json_file:
        inverted_index = json.load(json_file)


# In[ ]:




