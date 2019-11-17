#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import requests


# In[ ]:


from collector_utils import parse_movies, get_valid_links, crawl_wikipedia_pages


# In[ ]:


parse_movies()


# In[ ]:


get_valid_links()


# In[ ]:


crawl_wikipedia_pages()


# In[ ]:




