#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# We get all movies URL from movies2.html, movies3.html and movies1.html

def parse_movies():
    
    import pandas as pd
    from bs4 import BeautifulSoup
    import requests
    
    #movies2.html
    url = 'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies2.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.text,'html.parser')

    links_list2 = []

    for tag in soup.find_all('a'):
        links_list2.append(tag.get_text())
        
    #movies3.html

    url = 'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies3.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.text,'html.parser')
    
    links_list3 = []

    for tag in soup.find_all('a'):
        links_list3.append(tag.get_text())
        
    #movies1.html

    url = 'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.text,'html.parser')

    links_list1 = []

    for tag in soup.find_all('a'):
        links_list1.append(tag.get_text())
        
        
        
    # we merge the 3 lists
    links_list = links_list2 + links_list3 + links_list1
    
    # we create a dataframe to store the list
    df_movies = pd.DataFrame(links_list,columns = ['links'])
    
    


# In[ ]:


def get_valid_links():
    
    import pandas as pd
    # we create articles' names and add them to the dataframe

    article_list = []

    for i in range(1,30001):
        article = "article" + str(i) + ".html"
        article_list.append(article)
    
    df_movies['article'] = article_list
    
    # While trying to parse, we encounter some dead links. Let's drop them from our dataframe in order to avoid any error
    # Movies2 not found: 5521, 5576, 7726, 8101
    # Movies3 not found:  11268, 13665, 13965, 15241, 15874, 17676, 17721, 17722, 17769, 18054, 18181, 18274, 18379, 19230
    # Movies1 not found: 29430, 29672

    # We delete the dead links (20 in total)
    df_movies_final = df_movies.drop(df_movies.index[[5520, 5575, 7725, 8100, 11267, 13364, 13964, 15240, 15873, 17675, 17720, 17721, 17768, 18053, 18180, 18273, 18378, 19229, 29429, 29671]])


# In[ ]:


def crawl_wikipedia_pages():
    
    import pandas as pd
    import urllib.request
    
    # we crawl all our valid links, and write the content in new html files that we store on our computer

    for index,row in df_movies_final.iterrows():
    
        with urllib.request.urlopen(row['links']) as url:
            content = url.read()
        
        with open(row['article'], "wb") as f:
            f.write(content)
            f.close()
            
            
    # We create path for our files and store them in our dataframe

    url_list = []

    for index, row in df_movies_final.iterrows():
        url = r"C:\Users\Nathan\Sapienza\AMDM\HW3\Movies" + "\\" + row['article']
        url_list.append(url)
    
    df_movies_final['url'] = url_list

