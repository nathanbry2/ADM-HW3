#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# We import used libraries

import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import csv
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
import math


# In[ ]:


import import_ipynb
from utils import preprocess, load_files


# In[ ]:


final_df_movies = pd.read_csv('final_df_movies.csv')


# In[ ]:


load_files()


# In[ ]:


def search_engine1():
    
    # Search Engine 1


    query = input("What kind of film are you interested in?") #We ask the user to enter a query
    preprocessed_query = preprocess(query)# we preprocess the query


    result_doc_list = []
    # for each element of the query, we get the documents containing this element
    for word in preprocessed_query:
        if word not in list(simple_index.keys()):
            print("One word from your query is not in our words list")
            return



        if word in list(simple_index.keys()):
            ind = list(simple_index.keys()).index(word)
            result_doc = list(simple_index.values())[ind]
            result_doc_list.append(result_doc)

    #we only keep the documents containing all the elements of the query
    final_results_list = list(set(result_doc_list[0]).intersection(*result_doc_list[:len(result_doc_list)]))

    if len(final_results_list) == 0:
        print("No movie matching your query")
        return




    title_list = []
    intro_list = []
    url_list = []

    # we open our tsv files and extract the information for our movies
    for doc in final_results_list:

        with open(r'C:\Users\Nathan\Sapienza\AMDM\HW3\documents\\' + doc + '.tsv', encoding = 'utf8') as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:

                title = row['title']
                intro = row['intro']
                url = row['url']

                title_list.append(title)
                intro_list.append(intro)
                url_list.append(url)

    #we create a dataframe with these information        
    df_results = pd.DataFrame(list(zip(title_list, intro_list,url_list)), columns = ['Title', 'Intro', 'Wikipedia URL'])

    pd.set_option('display.max_rows', 500) #we display up to 500 results
    pd.set_option('max_colwidth', 300) #we displey up to 300 characters per row
    
    #and then we display our results
    df_results


# In[ ]:


def search_engine2():
    
    # Search Engine 2 (with similarity score)

    query = input("What kind of film are you interested in?") #We ask the user to enter a query
    preprocessed_query = preprocess(query) #we preprocess the query

    #for each elemn of the preprocessed query, we get its number of occurrences
    count_list = []

    for word in preprocessed_query:
        count_list.append(preprocessed_query.count(word))

    # and we create a dictionary  
    dic_count = dict(zip(preprocessed_query, count_list))


    dic_tfidf = {}
    #for each elem in the preprocessed_query, we compute its tfidf
    for key,value in dic_count.items():
        tf = value / len(preprocessed_query)
        dic_tfidf[key] = tf * (1 + math.log(29168 / len(inverted_index[key])))

    # for each element of the query, we get the documents containing this element
    result_doc_list = []

    for elem in preprocessed_query:
        if elem not in list(simple_index.keys()):
            print("One word from your query is not in our words list")
            return

        if elem in list(simple_index.keys()):
            ind = list(simple_index.keys()).index(elem)
            result_doc = list(simple_index.values())[ind]
            result_doc_list.append(result_doc)

    #we only keep the documents containing all the elements of the query
    final_results_list = list(set(result_doc_list[0]).intersection(*result_doc_list[:len(result_doc_list)]))

    if len(final_results_list) == 0:
        print("No movie matching your query")
        return

    #for each document containing all query's elements, 
    #we get the tfidf of each word in this specific doc, and store these info in a dictionary

    dic_final = {}

    for doc in final_results_list :
        dic_result = {}
        for elem in preprocessed_query:
            ind = list(simple_index.keys()).index(elem)
            dic_result[elem] = inverted_index[elem][doc]
        dic_final[doc] = dic_result




    #for each document, we compute its cosine similarity

    dic_cosine = {}

    for keys, values in dic_final.items():
        dot_product = 0
        norm_query = 0
        norm_doc = 0

        for key in dic_tfidf.keys():
            dot_product += values[key] * dic_tfidf[key]
            norm_query += dic_tfidf[key]**2
            norm_doc += values[key]**2

        norm_query = math.sqrt(norm_query)
        norm_doc = math.sqrt(norm_doc)

        cosine_similarity = dot_product / (norm_query*norm_doc)

        dic_cosine[keys] = cosine_similarity


    # we open our tsv files and extract the information for our movies

    title_list = []
    intro_list = []
    url_list = []
    cosine_list = []

    for doc in final_results_list:

        cosine = dic_cosine[doc]
        cosine_list.append(cosine)

        with open(r'C:\Users\Nathan\Sapienza\AMDM\HW3\documents\\' + doc + '.tsv', encoding = 'utf8') as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:

                title = row['title']
                intro = row['intro']
                url = row['url']

                title_list.append(title)
                intro_list.append(intro)
                url_list.append(url)


    # we create a dictionary with these information
    df_results = pd.DataFrame(list(zip(title_list, intro_list,url_list,cosine_list)), columns = ['Title', 'Intro', 'Wikipedia URL', 'Similarity'])

    pd.options.display.float_format = '{:,.2f}'.format #we display only two decimals for floats
    pd.set_option('display.max_rows', 500) #we display up to 500 results
    pd.set_option('max_colwidth', 300) #we displey up to 300 characters per row

    #and we display our results, sorted by their Similarity in descending order 
    df_results.sort_values(by=['Similarity'],ascending = False).reset_index(drop=True)


# In[ ]:


search_engine_number = int(input("Choose your search engine (1 or 2)"))

if search_engine_number == 1:
    launch = search_engine1()
elif search_engine_number == 2: 
    launch = search_engine2()
else:
    print("Please retry")
    
launch

