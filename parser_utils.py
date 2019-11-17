#!/usr/bin/env python
# coding: utf-8

# In[4]:


# After exploring the structure of some infobox, we notice that the values of the lists
# are not separated by tags or punctuation. For example we have Name1Name2: John DoeJane Doe, or John Doe (writer)Jane Doe

# We create a function that will split elements if:
# - a lower case letter is followed by an upper case letter
# - a lower case letter is followed by a digit
# - a ')' is followed by an upper case letter


def split_names(string):
    new_string = string
    index_list = []

    for i in range(len(string)-1):
        if (string[i].islower() == True & string[i+1].isupper() == True) | (string[i].islower() == True & string[i+1].isdigit() == True) | ((string[i]==')') == True & string[i+1].isupper() == True):
            index_list.append(i)
    j = 0
    for ind in index_list:
    
        new_string = new_string[:ind+1+j] + '_' + new_string[ind+1+j:]
        j += 1
    return new_string


# In[5]:


def parsing_tool():
    
    import pandas as pd
    from bs4 import BeautifulSoup
    
    # While parsing pages, we notice that some links do not point lead to Wikipedia film pages (14) 
    # So we drop them for our dataframe

    df_movies_new = df_movies.drop(df_movies.index[[5151,5574,8860,9921,11172,12244,12904,13658,17987,20035,20073,20117,28253,29297]]).reset_index(drop=True)
    
    
    
    
    #Here is our parsing tool

    # We create one list for all kind of information we want to extract
    title_list = []
    director_list = []
    producer_list = []
    writer_list = []
    actors_list = []
    music_list = []
    release_date_list = []
    runtime_list = []
    country_list = []
    language_list = []
    budget_list = []



    for index,row in df_movies_new.iterrows(): # we create a loop for all our articles
        soup = BeautifulSoup(open(row['url'],encoding="utf8"),'html.parser')
        infobox = soup.find('table', class_ = "infobox vevent") # we find the infobox
        if infobox is not None: #if there is indeed an infobox, we execute the following code

            list = infobox.find_all('tr') # we list all <tr> tags, this is the structure for each category in the infobox

            # The default values are False 
            director = False
            producer = False
            writer = False
            actors = False
            music = False
            release_date = False
            runtime = False
            country = False
            language = False
            budget = False


            title = list[0].get_text() #title is the first element of the <tr> tags list
            title_list.append([title])


            for elem in list[1:]:

                #for each category, we clean the info by deleting some useless elements
                lst = split_names(elem.get_text()).replace('\n','_').replace('[1]','').replace('[2]','').replace('[3]','').replace('[4]','').replace('[5]','').replace('[6]','').replace('[7]','').replace('[8]','').replace('[9]','').replace('[10]','').replace(u'\xa0', u' ').replace('$','_$').replace('€','_€').replace('£','_£').replace('₹','_₹').strip().split('_')

                new_lst = []
                for sub in lst: #and we append the cleaned info to a new list
                    if len(sub) > 0:
                        new_lst.append(sub)




                if len(new_lst) > 0: # we try go get our information. If one information is successfully found we set the value of its category as true     
                    if new_lst[0] == 'Directed by':
                        director_list.append(new_lst[1:])
                        director = True
                    if new_lst[0] == 'Produced by':
                        producer_list.append(new_lst[1:])
                        producer = True
                    if new_lst[0] == 'Written by':
                        writer_list.append(new_lst[1:])
                        writer = True
                    if new_lst[0] == 'Starring':
                        actors_list.append(new_lst[1:])
                        actors = True
                    if new_lst[0] == 'Music by':
                        music_list.append(new_lst[1:])
                        music = True
                    if new_lst[0] == 'Release date':
                        date = new_lst[1].split('(')[0].strip() #e only take the first release date
                        release_date_list.append([date])
                        release_date = True
                    if new_lst[0] == 'Running time':
                        duration = re.findall(r'\d+', new_lst[1]) #we extract only digits
                        runtime_list.append([int(duration[0])])
                        runtime = True
                    if new_lst[0] == 'Country':
                        country_list.append(new_lst[1:])
                        country = True
                    if new_lst[0] == 'Language':
                        language_list.append(new_lst[1:])
                        language = True    
                    if new_lst[0] == 'Budget':
                        budget_list.append(new_lst[1:])
                        budget = True    


            # if an info is missing (value of category == False), we append 'NA'
            if director == False:
                director_list.append(['NA'])
            if producer == False:
                producer_list.append(['NA'])
            if writer == False:
                writer_list.append(['NA'])
            if actors == False:
                actors_list.append(['NA'])
            if music == False:
                music_list.append(['NA'])
            if release_date == False:
                release_date_list.append(['NA'])
            if runtime == False:
                runtime_list.append(['NA'])
            if country == False:
                country_list.append(['NA'])
            if language == False:
                language_list.append(['NA'])
            if budget == False:
                budget_list.append(['NA'])

        else: # If there is no infobox, we add 'NA' to all values

            title_list.append(['NA'])
            director_list.append(['NA'])
            producer_list.append(['NA'])
            writer_list.append(['NA'])
            actors_list.append(['NA'])
            music_list.append(['NA'])
            release_date_list.append(['NA'])
            runtime_list.append(['NA'])
            country_list.append(['NA'])
            language_list.append(['NA'])
            budget_list.append(['NA'])  
            
      
    
    #we append our new information to our dataframe
    df_movies_new['title'] = title_list
    df_movies_new['director'] = director_list
    df_movies_new['producer'] = producer_list
    df_movies_new['writer'] = writer_list
    df_movies_new['actors'] = actors_list
    df_movies_new['music'] = music_list
    df_movies_new['release_date'] = release_date_list
    df_movies_new['runtime'] = runtime_list
    df_movies_new['country'] = country_list
    df_movies_new['language'] = language_list
    df_movies_new['budget'] = budget_list
    
    
    # We notice that some rows have 'NA' values for all columns including title, so they can't be used
    # We drop these rows (800)
    final_df_movies = df_movies_new[df_movies_new['title'] != '[\'NA\']'].reset_index(drop=True)
    
    
    # now we only have cleaned data!
    final_df_movies
    
    
    
    # Here is the code we use to get all intros

    # While exploring the structure of Wikipedia pages, we notice that the intro is always in 1 or several <p> tags
    # and these <p> are always BEFORE the first <h2> tag

    intro_list = []

    for index,row in final_df_movies.iterrows():

        soup = BeautifulSoup(open(row['url'],encoding="utf8"),'html.parser')

        all_tags = soup.find_all() # we create a list with all tags
        all_p = soup.find_all('p') # we create a list with all p tags
        all_h2 = soup.find_all('h2') # we create a list with all h2 tags


        # get intro p tags

        int_list = []

        first_h2_ind = all_tags.index(all_h2[0]) # we get the index of the first h2 tag in the list with all tags

        for elem in all_p: # and we get all p tags with and index smaller than the index of first h2 tag
            ind_p = all_tags.index(elem)
            if ind_p < first_h2_ind:
                int_list.append(elem)

        new_int_list = []
        for elem in int_list: # in the same way than what we did before while parsing infobox categories, we clean our intros...
            clean_elem = elem.get_text().replace('\n','').replace('[1]','').replace('[2]','').replace('[3]','').replace('[4]','').replace('[5]','').replace('[6]','').replace('[7]','').replace('[8]','').replace('[9]','').replace('[10]','').replace(u'\xa0', u' ')
            if clean_elem != '': # and if they're not empty, we append them to a new_list
                new_int_list.append(clean_elem)

        # if the list is empty, we append 'NA'         
        if len(new_int_list) == 0:
            new_int_list.append('NA')


        # and finally we append this list of p tags contents to our intro_list
        intro_list.append(new_int_list)
        
        
        
        
    # Here is the code we use to get all plots

    # While exploring the structure of Wikipedia pages, we notice that the plot is always in 1 or several <p> tags
    # and these <p> tags are always :
    # - FIRST CASE: between the second <h2> tag and the third one IF the first h2 is "Content" (followed by the table of content)
    # - SECOND CASE: between the first <h2> tag and the second one IF there is no table of contents

    plot_list = []

    for index,row in final_df_movies.iterrows():

        soup = BeautifulSoup(open(row['url'],encoding="utf8"),'html.parser')

        all_tags = soup.find_all() # we create a list with all tags
        all_p = soup.find_all('p') # we create a list with all p tags
        all_h2 = soup.find_all('h2') # we create a list with all h2 tags


        pl_list = []


        if 'Contents' in all_h2[0].get_text(): # we check if we are in the first case

            second_h2_ind = all_tags.index(all_h2[1]) # we get the index of the second h2 tag in the list with all tags
            third_h2_ind = all_tags.index(all_h2[2]) # we get the index of the third h2 tag in the list with all tags

            for elem in all_p: # and we get all p tags with and index greater than index of second h2 tag and smaller than the index of third h2 tag
                ind_p = all_tags.index(elem)
                if second_h2_ind < ind_p < third_h2_ind:
                    pl_list.append(elem)

            new_plot_list = []
            for elem in pl_list: # in the same way than what we did before while parsing infobox categories, we clean our plots...
                clean_elem = elem.get_text().replace('\n','').replace('[1]','').replace('[2]','').replace('[3]','').replace('[4]','').replace('[5]','').replace('[6]','').replace('[7]','').replace('[8]','').replace('[9]','').replace('[10]','').replace(u'\xa0', u' ')
                if clean_elem != '':# and if they're not empty, we append them to a new_list
                    new_plot_list.append(clean_elem)


        else: # if not first case, then second case

            first_h2_ind = all_tags.index(all_h2[0]) # we get the index of the first h2 tag in the list with all tags
            second_h2_ind = all_tags.index(all_h2[1]) # we get the index of the second h2 tag in the list with all tags


            for elem in all_p: # and we get all p tags with and index greater than index of first h2 tag and smaller than the index of second h2 tag
                ind_p = all_tags.index(elem)
                if first_h2_ind < ind_p < second_h2_ind:
                    pl_list.append(elem)

            new_plot_list = []
            for elem in pl_list:# in the same way than what we did before while parsing infobox categories, we clean our plots...
                clean_elem = elem.get_text().replace('\n','').replace('[1]','').replace('[2]','').replace('[3]','').replace('[4]','').replace('[5]','').replace('[6]','').replace('[7]','').replace('[8]','').replace('[9]','').replace('[10]','').replace(u'\xa0', u' ')
                if clean_elem != '':# and if they're not empty, we append them to a new_list
                    new_plot_list.append(clean_elem)

        # if the list is empty, we append 'NA'         
        if len(new_plot_list) == 0:
            new_plot_list.append('NA')

        # and finally we append this list of p tags contents to our plot_list
        plot_list.append(new_plot_list)
        
    
    
    # we add our new information to our dataframe
    final_df_movies['intro'] = intro_list
    final_df_movies['plot'] = plot_list


# In[6]:


def tsv_writer():
    
    import pandas as pd
    import csv
    # for each movie, we create a tsv file in which we write all information we have

    for index,row in final_df_movies.iterrows():
        title = row['title'].replace('[','').replace(']','').strip('\'')
        intro = row['intro'].replace('[','').replace(']','').replace('\'','').replace(',,',',').replace(', ,',',').replace('.\",','.').replace('.\',','.').replace('.\"','.').replace('.,','.').replace('\\','\'')
        plot = row['plot'].replace('[','').replace(']','').replace('\'','').replace(',,',',').replace(', ,',',').replace('.\",','.').replace('.\',','.').replace('.\"','.').replace('.,','.').replace('\\','\'')
        director = row['director'].replace('[','').replace(']','').replace('\'','')
        producer = row['producer'].replace('[','').replace(']','').replace('\'','')
        writer = row['writer'].replace('[','').replace(']','').replace('\'','')
        actors = row['actors'].replace('[','').replace(']','').replace('\'','')
        music = row['music'].replace('[','').replace(']','').replace('\'','')
        release_date = row['release_date'].replace('[','').replace(']','').replace('\'','')
        runtime = row['runtime'].replace('[','').replace(']','').replace('\'','')
        country = row['country'].replace('[','').replace(']','').replace('\'','')
        language = row['language'].replace('[','').replace(']','').replace('\'','')
        budget = row['budget'].replace('[','').replace(']','').replace('\'','')
        url = row['links'].replace('[','').replace(']','').strip('\'')



        with open('document' + str(row['article'][7:-5]) + '.tsv', 'wt', encoding = 'utf8') as f:
            tsv_writer = csv.writer(f, delimiter='\t')
            tsv_writer.writerow(['title','intro', 'plot','director', 'producer', 'writer', 'actors', 'music', 'release_date', 'runtime', 'country', 'language', 'budget', 'url'])
            tsv_writer.writerow([title, intro, plot, director, producer, writer, actors, music, release_date, runtime, country, language, budget, url])


# In[ ]:




