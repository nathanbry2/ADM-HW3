#!/usr/bin/env python
# coding: utf-8

# In[3]:


def preprocessing_intro_plot():
    
    import pandas as pd
    
    # for each movie, we preprocess its intro and plot

    preprocessed_intro_list = []
    preprocessed_plot_list = []

    for index,row in final_df_movies.iterrows():
        preprocessed_intro = preprocess(row['intro'])
        preprocessed_plot = preprocess(row['plot'])

        preprocessed_intro_list.append(preprocessed_intro)
        preprocessed_plot_list.append(preprocessed_plot)
        
    
    # and we store them in our dataframe
    final_df_movies['preprocessed_intro'] = preprocessed_intro_list
    final_df_movies['preprocessed_plot'] = preprocessed_plot_list
        


# In[4]:


def create_index():
    
    import pandas as pd
    import json
    
    # we create 2 index: 
    # 1st: the words are the keys and the values are lists of the documents containing each word
    # 2nd: the words are the keys and the values are lists of the documents containing each word + a count of the word in each document

    word_list = []
    doc_list = []
    doc_count_list = []

    for index,row in final_df_movies.iterrows():
        merge_preprocessed_intro_plot = row['preprocessed_intro'] + row['preprocessed_plot']
        for word in merge_preprocessed_intro_plot:
            if word not in word_list:
                word_list.append(word)
                doc_list.append(['document' + str(row['article'][7:-5])])
                doc_count_list.append([('document' + str(row['article'][7:-5]),merge_preprocessed_intro_plot.count(word))])

            if word in word_list:
                ind = word_list.index(word)
                doc = 'document' + str(row['article'][7:-5])
                if doc not in doc_list[ind]:
                    doc_list[ind].append('document' + str(row['article'][7:-5]))
                    doc_count_list[ind].append(('document' + str(row['article'][7:-5]),merge_preprocessed_intro_plot.count(word)))

                    
                    
    # We create our 2 index from the lists we just created
    simple_index = dict(zip(word_list, doc_list))
    count_index = dict(zip(word_list, doc_count_list))

    
    # we save our simple index into a json file
    with open("simple_index.json", 'w') as outfile:
        json.dump(simple_index, outfile)
        

    # we save our count index into a json file

    with open("count_index.json", 'w') as outfile:
        json.dump(count_index, outfile)


# In[5]:


def create_doc_count_words():
    
    import pandas as pd
    import json
    
    # we create a dictionary containing the count of words in each document

    doc_list = []
    count_list = []

    for index,row in final_df_movies.iterrows():
        intro_words = row['preprocessed_intro'].replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
        plot_words = row['preprocessed_plot'].replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')

        len_doc = len(intro_words) + len(plot_words)

        doc_list.append('document' + str(row['article'][7:-5]))
        count_list.append(len_doc)

    doc_count_words = dict(zip(doc_list, count_list))
    
    
    # we store this dictionary in a json file
    with open("doc_count_words.json", 'w') as outfile:
        json.dump(doc_count_words, outfile)


# In[6]:


def create_inverted_index():
    
    import pandas as pd
    import json
    
    # we create our interved index

    invert = []

    k = 0

    for key,value in count_index.items():
        dic = {}
        for element in value:
            doc = element[0]
            total_words = doc_count_words[doc]
            count = element[1]
            dic[doc] = (count/total_words)*(1 + math.log(29168/(len(value)))) #we compute the tfidf for each doc/word combination

        invert.append(dic) 
    
    inverted_index = dict(zip(word_list, invert))
    
    
    # and we save our inverted index in a json file

    with open("inverted_index.json", 'w') as outfile:
        json.dump(inverted_index, outfile)    

