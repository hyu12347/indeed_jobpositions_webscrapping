#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from time import time, sleep
from random import randint
from warnings import warn
from IPython.core.display import clear_output
import numpy as np


# In[2]:


job_title=[]
company=[]
job_location=[]
salary=[]
job_description=[]
date_post=[]
rating_company=[]


# In[3]:


job_titles = ['Data Analyst', 'Data Scientist', 'Database Administrator', 'Machine Learning Engineer', 'Data Engineer']
states = ['Virginia', 'New York', 'California', 'Texas', 'Washington State']


# In[4]:


start_time = time()
request = 0


# In[5]:


for state in states:
    for job in job_titles:
        response = get('https://www.indeed.com/jobs?q='+job+'&l='+state+'&sort=date')
        sleep(randint(8,15))
        request += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(request, request/elapsed_time))
        clear_output(wait = True)

        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(request, response.status_code))

        if request > 100:
            warn('Number of requests was greater than expected.')
            break

        bs = BeautifulSoup(response.text, 'html.parser')

        job_containers = bs.find_all('div', {'class': {'job_seen_beacon'}})

        for container in job_containers:

        #job_title
            try:
                jt = container.find("div",{"class":{"heading4"}})
                job_title.append(jt.text)
                #print(jt.text)
            except:
                job_title.append("Missing")
                                
        #company
            try:
                com = container.find("span",{"class":{"companyName"}})
                company.append(com.text)
            except:
                company.append("Missing")
        #job_location
            try:
                loc = container.find("div",{"class":{"companyLocation"}})
                #print(loc.text)
                job_location.append(loc.text)
            except:
                job_location.append("Missing")
        #salary
            try:
                sal = container.find("div",{"class":{"attribute_snippet"}})
                salary.append(sal.text)
            except:
                salary.append("Missing")
        #job_description
            try:
                job_des = container.find("div",{"class":{"job-snippet"}})
                job_description.append(job_des.text)
            except:
                job_description.append("Missing")
        #date_post
            try:
                datepo = container.find("span",{"class":{"date"}})
                date_post.append(datepo.text)
            except:
                date_post.append("Missing")
        #rating_company
            try:
                rate = container.find("span",{"class":{"ratingNumber"}})
                rating_company.append(rate.text)
            except:
                rating_company.append("Missing")


# In[6]:


date_post


# In[7]:


job_list = pd.DataFrame({
    "Job title":job_title,
    "Company Name": company,
    "Job Location": job_location,
    "Salary": salary,
    "Job Discription": job_description,
    "Date": date_post,
    "Rate": rating_company
})
job_list


# In[8]:


job_list = job_list.join(job_list["Job Location"].str.split(",",expand=True).add_prefix("city").fillna(np.nan))
job_list


# In[ ]:





# In[9]:


job_list['Job title']=job_list['Job title'].str.replace(r'(^.*Data Analyst.*$)', 'Data Analyst')
job_list['Job title']=job_list['Job title'].str.replace(r'(^.*Data Scientist.*$)', 'Data Scientist')
job_list['Job title']=job_list['Job title'].str.replace(r'(^.*Database Administrator.*$)', 'Database Administrator')
job_list['Job title']=job_list['Job title'].str.replace(r'(^.*Machine Learning Engineer.*$)', 'Machine Learning Engineer')
job_list['Job title']=job_list['Job title'].str.replace(r'(^.*Data Engineer.*$)', 'Data Engineer')
job_list['Job title']


# In[10]:


job_list.head()


# In[11]:


np.round(pd.crosstab(job_list['city0'], job_list['Job title'], normalize='index') * 100,2)


# In[12]:


job_list.to_csv("C:/Users/Cici/Downloads/PA4.csv")


# In[ ]:




