#!/usr/bin/env python
# coding: utf-8

# # Assignment 2: Milestone I Natural Language Processing
# ## Task 1. Basic Text Pre-processing
# #### Student Name: Syeda Shabnam Khan
# #### Student ID: 000000
# 
# Date: 17-05-2024
# 
# Version: 1.0
# 
# Environment: Python 3 and Jupyter notebook
# 
# Libraries used: 
# * pandas
# * re
# * numpy
# * scikitlearn
# * nltk
# * itertools
# 
# ## Introduction
# This is the first of 3 task for this assessment. We are doing basic text processing on some job advertisements. We have downloaded 776 document. There are four folders namely: Accounting_Finance, Engineering, Healthcare_Nursing, and Sales. Each are named after job category. the objective of this task is to use appropriate libraries and functions to extract, tokenize and preprocess the documents. Then generate an output of the vocabulary and save it in the specified format.

# ## Importing libraries 

# In[1]:


# Code to import libraries as you need in this assessment, e.g.,
from sklearn.datasets import load_files
import numpy as np
from nltk import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from itertools import chain
import re
from nltk.probability import *
import pandas as pd


# ### 1.1 Examining and loading data
# In this section we load and examine the data folders. We used the load files from sklearn to load the documents. We have 1 folder named data with 4 subfolders. These subfolders hold their corresponding job advertisement. When we use load_file() and pass the folder 'data' it reads the subfolder names as target variables and each text file with is read as data or rows.

# Based on the file path we can see that the target and filenname matches. The data folder contains 4 sub-folders: 'Accounting_Finance', 'Engineering', 'Healthcare_Nursing', 'Sales'. The load_files function from sklearn.datasets was used to read the names of the sub-folders as target variables and the text files contained in it as filenames. The target values 0, 1, 2, 3 represent the sub-folders 'Accounting_Finance', 'Engineering', 'Healthcare_Nursing', 'Sales' respectively.      
# There is a total of 776 text files. The number of files in each sub-folder are:  
# - Accounting_Finance: 191
# - Engineering: 231 
# - Healthcare_Nursing: 198
# - Sales: 156  
# 
# The content in the text file starts with *b'Title:* or *b"Title:*, where b' represents byte. This need to be decoded into string before we can do anything else. 

# In[2]:


# saving the files as job_data
job_data = load_files(r"data")


# In[3]:


# Display the first 10 job data
job_data['filenames'][0:10]


# In[4]:


# The subfolfers are read as targets
# Display the target values of the first 10 job data
job_data['target'][0:10]


# In[5]:


# The target names of our data
job_data['target_names']


# In[6]:


# We will take an example to see wether the data matches
job_data['filenames'][15], job_data['target'][15]


# In[7]:


# Number of files in the data folder
len(job_data['filenames'])


# In[8]:


# Counting the number of text files in each folder
np.unique(job_data['target'], return_counts = True)


# In[9]:


# Looking at the data inside job_data
job_data.data


# In[10]:


job_data.data[3:5]


# In[11]:


# storing the data and target values in list
# job_ad has the job description and 
# category has the target or sub-folder name
# represented by number
job_ad, category = job_data.data, job_data.target


# In[12]:


job_ad[10], category[10]


# In[13]:


# Function to decode binary to string 
# And case normalization to lower case
def decode_lower(raw_ad):
#     Convert the byte likr data to string
    job_ad = raw_ad.decode('utf-8')  
#     Convert the words to lower case
    job_ad = job_ad.lower() 
    
    return job_ad


# In[14]:


decoded_ad = [decode_lower(r) for r in job_ad]


# In[15]:


decoded_ad


# #### Extract title, webindex, company name and description
# 
# Now that we have our ad decoded, we will extract the title, webindex, company and description. From initial examination, all of the ads have title, webindex and description. However, some ads have company and some do not. We extract the data into lists and fill any missing values with 'not specified'.

# In[16]:


title = []
webindex = []
company =[]
description = []

# function to extract the data into appropriate column
# using regex to extract data because I want to capture
# the information and exclude the name
# e.g., from title: scrub nurse, we will only keep scrub nurse 
def column_extractor(ad):
    list_ad = re.split(r"\n", ad)
    title.append(re.findall(r'title: (.*)', list_ad[0])[0])
    webindex.append(re.findall(r'webindex: (.*)', list_ad[1])[0])
    if len(list_ad)<4:
        company.append('not specified')
        description.append(re.findall(r'description: (.*)', list_ad[2])[0])
    else:
        company.append(re.findall(r'company: (.*)', list_ad[2])[0])
        description.append(re.findall(r'description: (.*)', list_ad[3])[0])


# In[17]:


# extracting data
for c in decoded_ad:   
    column_extractor(c)


# In[18]:


# Printing to check if the lists 
# are appended correctly
idx=6
print(title[idx])
print(webindex[idx])
print(company[idx])
print(description[idx])


# #### Tokenizing descriptions
# Now we need to tokenize the descriptions using the regex provided. For this we will use the RegexpTokenizer from nltk.

# In[19]:


# defining a function to tokenize the descriptions
# uses sent_tokenize from nltk to convert the descriptions into sentences
# then iterates the RegexpTokenizer over each sentence
def tokenizeAds(raw_desc):    
    # segment into sentences
    sentences = sent_tokenize(raw_desc)
    
    # tokenize each sentence
    pattern = r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?"
    tokenizer = RegexpTokenizer(pattern) 
    token_lists = [tokenizer.tokenize(sen) for sen in sentences]
    
    # merge them into a list of tokens
    tokenised_desc = list(chain.from_iterable(token_lists))
    return tokenised_desc


# In[20]:


# looping over the list description to get tokenized ad descriptions
tk_ads = [tokenizeAds(r) for r in description]


# In[21]:


# print the raw string and tokenized description for comparison
idx=5
print(f'Raw ad description at index {idx}: \n{description[idx]}')
print(f'Tokenized description at index {idx}: \n{tk_ads[idx]}')


# In[22]:


# Defining a function to print stats
# this will be a handy tool for us to observe the changes
# after each preprocessing step
def stats_print(tk_ads):
# put all the tokens in a single list
    words = list(chain.from_iterable(tk_ads))
# use set to create a list of unique words
# present in the tokens
    vocab = set(words) 
    lexical_diversity = len(vocab)/len(words)
    print("Vocabulary size: ",len(vocab))
    print("Total number of tokens: ", len(words))
    print("Lexical diversity: ", round(lexical_diversity,3))
    print("Total number of ad descriptions:", len(tk_ads))
    lens = [len(ad) for ad in tk_ads]
    print("Average description length:", np.mean(lens).round(3))
    print("Maximun description length:", np.max(lens))
    print("Minimun description length:", np.min(lens))
    print("Standard deviation of descriptions length:", np.std(lens).round(3))        


# In[23]:


# print the stats of the tokenized description
# before preprocessing
stats_print(tk_ads)


# ### 1.2 Pre-processing data
# In this section, we perform the required text pre-processing steps.

# Now that we have the description tokenized, we can iterate over the tokens to perform preprocessing such as removing less frequent words, stop words, etc.

# #### Remove words with length less than 2
# 
# We want to remove the words that have length less than 2 (e.g., a, e, etc). These words do not hold much meaning but takes up space in our vocabulary, therefore we need to remove them.

# In[24]:


# defining a function to find vocabulary
# we can use this to generate vocabulary after each preprocessing step
def vocab_finder(tokenized_list):
    words = list(chain.from_iterable(tokenized_list))
    # vocabulary of all words
    return sorted(list(set(words)))


# In[25]:


# creating the vocabulary
vocab = vocab_finder(tk_ads)
# making a list of words with lenth less than 2
filter_less_than_two = []
for word in vocab:
    if len(word)<2:
        filter_less_than_two.append(word)


# In[26]:


# removing words with length less than 2
# defining a filter that takes a token and a list of words as input
# it filters words from the token based on the filter list
def word_filter(description, filter_list):
    return [w for w in description if w not in filter_list]


# In[27]:


# iterating the word filter function over the list of token
# used filter_less_than_two as a filter list
tk_ads = [word_filter(description, filter_less_than_two) for description in tk_ads]
stats_print(tk_ads)


# Comparing the statistics with the statistics of the original tokenised document, the vocabulary size has decreased. Maximum length of descriptions and average description has also decreased.

# #### Removing Stopwords
# 
# We want to remove the stopword using the stopwords_en text file. These are the words that occur frequently in language but do not hold much meaning. therefore, removing them will reduce noise from our data.

# In[28]:


# Reading the file for Stopwords
stopwords = []
with open('./stopwords_en.txt') as f:
    stopwords = f.read().splitlines()


# In[29]:


# looking at how many words there are in the document
len(stopwords)


# In[30]:


# filtering the stopwords
tk_ads = [word_filter(description, stopwords) for description in tk_ads]
stats_print(tk_ads)


# After this step, the standard deviation has drastically decreased.

# #### Remove words that appear once based on term frequency
# 
# We want to remove words that appear only once in the document. Since their frequency is less, we can infer that they are not very important. This will make the vocabulary smaller, remove redundancy and reduce the size of word vector we will eventually generate.

# In[31]:


# making a list of words from the tokens to use
# for finding frequency distribution
words = list(chain.from_iterable(tk_ads))
# using FreqDist from nltk.probability
term_fd = FreqDist(words)


# In[32]:


# creating a list of words that appear only once
words_once = set(term_fd.hapaxes())
words_once


# In[33]:


# taking a look at how many words there are 
# that appears only once in the document
len(words_once)


# In[34]:


# filtering the words that appear only once
tk_ads = [word_filter(description, words_once) for description in tk_ads]


# In[35]:


# printing the stats to see changes
stats_print(tk_ads)


# After removing words that appear once the vocabulary size decreased drastically.

# #### Removing 50 most frequent words based on document frequency
# 
# We want to remove 50 words that appear most frequently across the documents. This will reduce noise in the document and help us focus on more meaningful words.

# In[36]:


# making a list of most frequent words based on
# document frequency
words_2 = list(chain.from_iterable([set(ad) for ad in tk_ads]))
doc_fd = FreqDist(words_2)  # compute document frequency for each unique word/type
doc_fd.most_common(50)


# In[37]:


# saves the first element from the list of tupple 
# that doc_fd.most_common(50 returns)
most_common = [word for word,freq in doc_fd.most_common(50)]


# In[38]:


# used the most common words to filter the tokens
tk_ads = [word_filter(description, most_common) for description in tk_ads]


# In[39]:


stats_print(tk_ads)


# Performing this step increased the lexical diversity of our document as evident from the statistics.

# #### Save all advertisement text and information
# We want to save all the information we extracted in a format that can be used in the future. In this case we are using a pandas dataframe and then saving the dataframe as a csv file. For convenience, we are saving the title, webindex, company and the raw description as extracted. Additionally, we will save the tokenized description and the target. For tokenized description, I am saving it as a list of string in tokens and also as normal string where each token is joined by a space. Although this creates some redundancy, it will lessen the data manipulation steps we need to do in the next step. Similarly, I have created one column for the numerical representation of the targets and another with target name.

# In[40]:


# The tokens are in a list of lists
# we want a simple list with the tokens as string
# for every document the string is joined with space
# each document will make a seperate item on the list
description_tk = [' '.join(t) for t in tk_ads]


# In[41]:


# assigning target name to the corresponding targets
category_name = [job_data.target_names[i] for i in job_data.target]


# In[42]:


# creating a dataframe using the tokens, 
# title, target and other information extracted
data ={'title' : title,
       'webindex' : webindex,
       'company' : company,
       'description_raw' : description,
       'description_tk' : description_tk,
       'tokens' : tk_ads,
       'target_name' : category_name,
       'target' : category
      }
df = pd.DataFrame(data)


# In[43]:


df.head()


# In[44]:


# checking if there are any null values
df.isnull().sum()


# In[45]:


# saving the dataframe as csv
df.to_csv('ads.csv', index=False)


# ## Saving required outputs
# Saving the vocabulary txt as per spectification.
# - vocab.txt

# In[46]:


# using my vocab_finder function to create a list of vocabulary
# the function gives a sorted list, so no need to sort again
vocab = vocab_finder(tk_ads)

# file name to save as
file_name = 'vocab.txt'

# creating the text file in format
# word_string:word_integer_index
with open(file_name, 'w') as file:
    for index, word in enumerate(vocab):
        file.write(f"{word}:{index}\n")


# ## Summary
# In this task, we extracted the data from the documents saved in the 'data' file. Then inspected and took appropriate measures to put them into lists. Used the list to tokenize and perform text preprocessing to remove word that express little  to no meaning. Finally the vocabulary of the word is saved in required format.

# ## References
# - COSC2820 Advanced Programming for Data Science. (2024). RMIT University
