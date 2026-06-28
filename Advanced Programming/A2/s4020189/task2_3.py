#!/usr/bin/env python
# coding: utf-8

# # Assignment 2: Milestone I Natural Language Processing
# ## Task 2&3
# #### Student Name: Syeda Shabnam Khan
# #### Student ID: s4020189
# 
# Date: 17-05-2024
# 
# Version: 1.0
# 
# Environment: Python 3 and Jupyter notebook
# 
# Libraries used: please include all the libraries you used in your assignment, e.g.,:
# * pandas
# * re
# * numpy
# * scikit learn
# * itertools
# * nltk
# * scipy
# * gensim
# * matplotlib
# 
# ## Introduction
# 
# In this part of the assignment we used the preprocessed data from task one to generate feature representation. Then use classification model to train on the features we extracted. Finally, conducted experiments to see how the language models compare and whether more information gives better accuracy.
# 

# ## Importing libraries 

# In[1]:


# Code to import libraries as you need in this assessment, e.g.,
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim.downloader as api
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from nltk.tokenize import sent_tokenize
from itertools import chain
from nltk.tokenize import RegexpTokenizer
from nltk.probability import *
from scipy.sparse import hstack
import matplotlib.pyplot as plt


# In[2]:


import warnings
warnings.filterwarnings("ignore")
# to supress the warnings we get


# ## Task 2. Generating Feature Representations for Job Advertisement Descriptions

# In task 2 we take the data saved in task 1 and create feature representation using count vectorizer, gloVe-wiki-gigaword-100 and tf-idf weighted vector with glove-wiki-gigaword-100.

# In[3]:


# Reading the data from task 1
data = pd.read_csv('ads.csv')
data.head()


# In[4]:


# Converting our tokenized description to a list
# this is requireds because count vectorizer takes a list as argument
tk_ads = data['description_tk'].tolist()


# In[5]:


# using the file saved in task 1
with open('vocab.txt', 'r') as file:
    # Read the lines of the file into a list
    lines = file.readlines()

# extract each line into a list of word
# and a list of index
vocab = [(line.strip().split(':')[0]) for line in lines]
vocab_index =[(line.strip().split(':')[1]) for line in lines]


# In[6]:


# to ensure the features are aligned with task 1
# make a dictionary of the vocabulary with index
vocab_dict = {word: idx for word, idx in zip(vocab, vocab_index)}
# makes a orderless directory of word and its corresponding index


# In[7]:


tokens = data['tokens']
tokens


# #### Using count vector

# In[8]:


# initiating the count vectorizer
cVec = CountVectorizer(analyzer = "word",vocabulary = vocab)


# In[9]:


# fitting the list of tokens to count vectorizer
features_cv = cVec.fit_transform(tk_ads)
features_cv.shape


# In[10]:


# defining a function to print the word and their corresponding 
# values from vectoring
def print_vector(vector_output,idx=0):
    for word, value in zip(vocab, vector_output.toarray()[idx]): 
        if value > 0:
            print(word+":"+str(value), end =' ')


# In[11]:


print_vector(features_cv,2)


# #### Tf-idf vector to calculate the weights

# In[12]:


# Initializing the tfidf vectorizer to calculate the
# tfidf weights og the vocabulary
tVec = TfidfVectorizer(analyzer = "word",vocabulary = vocab) # initialised the TfidfVectorizer
tfidf_features = tVec.fit_transform(tk_ads) 
tfidf_features.shape


# In[13]:


print_vector(tfidf_features,2)


# In[14]:


# See the the output type of the vectorizer
# this is important because to find weighted vector
#  we need to multiply this output
# inconsistent data format may create issues
type(tfidf_features)


# #### GloVe wiki gigaword 100
# We decided to go with glove-wiki-gigaword-100 because it is sufficiently light weight to handle in the laptop. Moreover, it is trained on  wikipedia and commoncrawl corpora and generates vector based on the statistical co-occurance of words.

# In[15]:


# downloading glove using gensim
gloveVec = api.load('glove-wiki-gigaword-100')


# In[16]:


# this gives the 100 vectors for the word flexible
gloveVec['flexible']


# In[17]:


# Function to generate document vector using glove model
# this will give the unweighted vectors
# The code for this function was taken from the class materials
def gen_docVecs(wv,tk_txts): # generate vector representation for documents
    docs_vectors = pd.DataFrame() # creating empty final dataframe
#     we will store the vectors in this dataframe
    for i in range(0,len(tk_txts)):
        tokens = tk_txts[i]
        temp = pd.DataFrame()  # creating a temporary dataframe(store value for 1st doc & for 2nd doc remove the details of 1st & proced through 2nd and so on..)
        for w_ind in range(0, len(tokens)): # looping through each word of a single document and spliting through space
            try:
                word = tokens[w_ind]
                word_vec = wv[word] # if word is present in embeddings then proceed
                temp = temp.append(pd.Series(word_vec), ignore_index = True) # if word is present then append it to temporary dataframe
            except:
                pass
        doc_vector = temp.sum() # take the sum of each column
        docs_vectors = docs_vectors.append(doc_vector, ignore_index = True) # append each document value to the final dataframe
    return docs_vectors


# In[18]:


# running the glove model
unweighted_vec =gen_docVecs(gloveVec,tokens)


# In[19]:


# any null values?
unweighted_vec.isna().any().sum()


# In[20]:


unweighted_vec.shape


# In[21]:


# the output is a pandas dataframe
type(unweighted_vec)


# #### Tf-idf weighted vector
# We will calculate tf-idf weighted vector for the descriptions

# In[22]:


# convert sparse matrix to dictionary of keys(dok)
# refer: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.dok_matrix.todok.html#scipy.sparse.dok_matrix.todok
# https://stackoverflow.com/questions/55373331/how-to-transform-a-scipy-sparse-matrix-to-a-dictionary
dok_matrix = tfidf_features.todok()


# In[23]:


dok_matrix


# In[24]:


dok_matrix.items()
# the dok_matrix is in the form of 
# (document index, term/word index), tfidf value


# In[25]:


tfidf_dict = {}

# Populate the dictionary with the TF-IDF weights
# for every item in our dok matrix, we iterate over the 
# document index, term index and tfidf weight
# get the corresponding feature name from the tfidf vectorizer
# if the document is not in the dictionary then put it as a key in dictionary
# then inside that key, save the term and weight as key value pair
for (doc_index, term_index), value in dok_matrix.items():
    # Get the term corresponding to the term_index
    term = tVec.get_feature_names_out()[term_index]
    if doc_index not in tfidf_dict:
        tfidf_dict[doc_index] = {}
    tfidf_dict[doc_index][term] = value


# In[26]:


# we now have a dictionary of dictionaries
# this will be used to match and multipy the weights for each token
tfidf_dict[0]


# In[27]:


# extended version of the `gen_docVecs` function
def gen_docVecs(wv,tk_txts,tfidf = []): # generate vector representation for documents
    docs_vectors = pd.DataFrame() # creating empty final dataframe
    #stopwords = nltk.corpus.stopwords.words('english') # removing stop words

    for i in range(0,len(tk_txts)):

        temp = pd.DataFrame()  # creating a temporary dataframe(store value for 1st doc & for 2nd doc remove the details of 1st & proced through 2nd and so on..)
        for w_ind in range(0, len(vocab)): # looping through each word of a single document and spliting through space
            try:
                word = vocab[w_ind]
                word_vec = wv[word] # if word is present in embeddings(goole provides weights associate with words(300)) then proceed
                
                if tfidf != []:
                    word_weight = float(tfidf[i][word])
                else:
                    word_weight = 1
                temp = temp.append(pd.Series(word_vec*word_weight), ignore_index = True) # if word is present then append it to temporary dataframe
            except:
                pass
        doc_vector = temp.sum() # take the sum of each column(w0, w1, w2,........w300)
        docs_vectors = docs_vectors.append(doc_vector, ignore_index = True) # append each document value to the final dataframe
    return docs_vectors


# In[28]:


weighted_vec =gen_docVecs(gloveVec,tokens,tfidf_dict)


# In[29]:


weighted_vec.shape


# In[30]:


weighted_vec.isnull().any().sum()


# ### Saving outputs
# Save the count vector representation as per spectification.
# - count_vectors.txt

# In[31]:


# code to save output data...
def write_vectorFile(data_features,filename):
    num = data_features.shape[0] # the number of document
    out_file = open(filename, 'w') # creates a txt file and open to save the vector representation
    for a_ind in range(0, num): # loop through each article by index
        w_idx = data['webindex'][a_ind]
        out_file.write("#{},".format(w_idx))
        for f_ind in data_features[a_ind].nonzero()[1]: # for each word index that has non-zero entry in the data_feature
            value = data_features[a_ind][0,f_ind] # retrieve the value of the entry from data_features
            out_file.write("{}:{} ".format(f_ind,value)) # write the entry to the file in the format of word_index:value
        out_file.write('\n') # start a new line after each article
    out_file.close() # close the file


# In[32]:


cVector_file = "./count_vectors.txt" # file name of the count vector
write_vectorFile(features_cv,cVector_file)


# ## Task 3. Job Advertisement Classification

# In this task we use classification machine learning models to observe the performence of the word vectorization techniques we used.

# In[33]:


# First we extract the target values from the pandas dataframe
# and read it as a numpy array to pass to the machine learning model
target = data['target'].values
target[0:5]


# In[34]:


# Setting the random seed to ensure that the results are reproduceable
seed = 99


# #### Training with count vector
# We first use the sparse matrix from count vectorizer

# In[35]:


# Splitting our data into 70-30 ratio
# 70% for training and 30% for testing
X_train, X_test, y_train, y_test,train_indices,test_indices =  train_test_split(features_cv, target, 
                                                                                list(range(0,len(target))),test_size=0.3,
                                                                                random_state =seed)


# In[36]:


# printing the test train indices
print(f'train: {train_indices}\n\ntest: {test_indices}')


# In[37]:


# we fit the training data
model = LogisticRegression(random_state=seed)
model.fit(X_train, y_train)


# In[38]:


# this gives theaccuracy score of the model using test data
# pretty good accuracy
count_accuracy =model.score(X_test,y_test)
count_accuracy


# #### Training with  unweighted glove-wiki-100
# We will use the glove vector this time

# In[39]:


# converting pandas df to numpy array
unweighted_glove =unweighted_vec.values
unweighted_glove


# In[40]:


unweighted_glove.shape


# In[41]:


type(unweighted_glove)


# In[42]:


X_train, X_test, y_train, y_test,train_indices,test_indices =  train_test_split(unweighted_glove, target, list(range(0,len(target))),test_size=0.3,
                                                                                random_state =seed)


# In[43]:


# printing the index will show that we have the same split for train-test
# this is done to ensure that the variation is due to the models and not due to the 
# train-test split
print(f'train: {train_indices}\n\ntest: {test_indices}')


# In[44]:


# fitting the glove vectors this time
model.fit(X_train, y_train)


# In[45]:


# the accuracy is quite low
unglo_accuracy =model.score(X_test,y_test)
unglo_accuracy


# #### Weighted Glove
# Finally we see test the weighted vector we calculated.

# In[46]:


# converting pandas df to numpy array
weighted_glove =weighted_vec.values
weighted_glove


# In[47]:


X_train, X_test, y_train, y_test,train_indices,test_indices =  train_test_split(weighted_glove, target, list(range(0,len(target))),test_size=0.3,
                                                                                random_state =seed)


# In[48]:


print(f'train: {train_indices}\n\ntest: {test_indices}')


# In[49]:


# fitting the weighted vectors
model.fit(X_train, y_train)


# In[50]:


# better than unweighted accuracy
w_glo_accuracy =model.score(X_test,y_test)
w_glo_accuracy


# #### Using k-fold for validation
# We have seen the accuracy for each model so far. The count vector performed nest followed by weighted count vector. We want to make sure this is not because of some lucky random train-test split. Therefore, we will use k-fold to validate our results.

# In[51]:


# initiating k folds
num_folds = 5
kf = KFold(n_splits= num_folds, random_state=seed, shuffle = True) # initialise a 5 fold validation
print(kf)


# In[52]:


# function to call the classification model
def evaluate_reg(X_train,X_test,y_train, y_test,seed):
    model = LogisticRegression(random_state=seed)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)


# In[53]:


# running the model on all three types of vectors 
# and saving the results as dataframe
num_models = 3
cv_df = pd.DataFrame(columns = ['count','glove','w_glove'],index=range(num_folds)) # creates a dataframe to store the accuracy scores in all the folds

fold = 0
for train_index, test_index in kf.split(list(range(0,len(target)))):
    y_train = [target[i] for i in train_index]
    y_test = [target[i] for i in test_index]

    X_train_count, X_test_count = features_cv[train_index], features_cv[test_index]
    cv_df.loc[fold,'count'] = evaluate_reg(features_cv[train_index],features_cv[test_index],y_train,y_test,seed)
    
    X_train_glo, X_test_glo = unweighted_glove[train_index], unweighted_glove[test_index]
    cv_df.loc[fold,'glove'] = evaluate_reg(unweighted_glove[train_index],unweighted_glove[test_index],y_train,y_test,seed)

    X_train_w_glo, X_test_w_glo = weighted_glove[train_index], weighted_glove[test_index]
    cv_df.loc[fold,'w_glove'] = evaluate_reg(weighted_glove[train_index],weighted_glove[test_index],y_train,y_test,seed)
    
    fold +=1


# In[54]:


#  the results shoe count performs better in every instance
cv_df


# In[55]:


# Plotting the results
plt.figure(figsize=(7, 5))

# Plot each feature representation
plt.plot(cv_df.index, cv_df['count'], marker='o', label='Count vector', color='skyblue')
plt.plot(cv_df.index, cv_df['glove'], marker='o', label='Unweighted glove model', color='salmon')
plt.plot(cv_df.index, cv_df['w_glove'], marker='o', label='Tf-Idf weighted model', color='lightgreen')

# Adding titles and labels
plt.title('Model Performance Comparison', fontsize=12)
plt.xlabel('Fold', fontsize=10)
plt.ylabel('Accuracy', fontsize=10)

# Adding legend
plt.legend(fontsize=10)

# Show the plot
plt.grid(True)
plt.xticks(cv_df.index, fontsize=10)
plt.yticks(fontsize=10)
plt.ylim(0, 1)  # Set y-axis range from 0 to 1 for better readability

plt.show()


# Based on the results plotted we can see that count vector performs the best. The tf-idf weighted vector using glove performs decently but the unweighted model has quite low accuracy. 

# #### To check whether more information is better 
# We conduct addition experiment to see if adding the title will give us a better result. But first we will preprocess the title using the same steps as task 1 to ensure rigour in our method.

# In[56]:


#  converting the dataframe to list
title = data['title'].tolist()
title


# In[57]:


# tokenizing title using the same tokenizer used for task 1
def tokenizeTitle(raw_title):    
    # segament into sentences
    sentences = sent_tokenize(raw_title)
    
    # tokenize each sentence
    pattern = r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?"
    tokenizer = RegexpTokenizer(pattern) 
    token_lists = [tokenizer.tokenize(sen) for sen in sentences]
    
    # merge them into a list of tokens
    tokenised_title = list(chain.from_iterable(token_lists))
    return tokenised_title


# In[58]:


tk_title = [tokenizeTitle(r) for r in title]
tk_title[0:5]


# In[59]:


# vocabulary of title
# defining a function to find vocabulary
def vocab_finder(tokenized_list):
    words = list(chain.from_iterable(tokenized_list))
    # vocabulary of all words
    return sorted(list(set(words)))


# In[60]:


# Creating the vocabulary for the title
title_vocab = vocab_finder(tk_title)


# In[61]:


# Preprocessing title
# making a list of words with lenth less than 2
one_letter_word = []
for word in title_vocab:
    if len(word)<2:
        one_letter_word.append(word)


# In[62]:


# difining a filter function
def word_filter(description, filter_list):
    return [w for w in description if w not in filter_list]


# In[63]:


# filtering all single letter words
tk_title = [word_filter(t, one_letter_word) for t in tk_title]


# In[64]:


# Reading the file for Stopwords
stopwords = []
with open('./stopwords_en.txt') as f:
    stopwords = f.read().splitlines()


# In[65]:


# filtering the stopwords
tk_title = [word_filter(t, stopwords) for t in tk_title]


# In[66]:


# making a list of words from the tokens to use
# for finding frequency distribution
title_words = list(chain.from_iterable(tk_title))
# using FreqDist from nltk.probability
term_fd = FreqDist(title_words)

# creating a list of words that appear only once
words_once = set(term_fd.hapaxes())


# In[67]:


# filtering the words that appear only once
tk_title = [word_filter(t, words_once) for t in tk_title]


# In[68]:


list_tk_title = [' '.join(t) for t in tk_title]


# In[69]:


# there are some empty string in the list
# not doing any further preprocessing to keep 
# the results consistent with description
list_tk_title


# #### Count vectors for title
# For this experiment we are using count vectorizer because it gave us the best accuracy in the previous part. First we find the count vectors for the title. Since we want to see which performs better, title only, title and description or just description, we need a vector for both count and title together. We horizontally stack the vectors we got from title  and description to generate one.

# In[70]:


# building the vector on the title vocabulary
cVec2 = CountVectorizer(analyzer = "word",vocabulary = title_vocab)


# In[71]:


count_title = cVec2.fit_transform(list_tk_title)
count_title.shape


# In[72]:


# Combining the sparse matrix we got for title 
# with the one we got for description
combined_count_vectors = hstack((count_title, features_cv))
combined_count_vectors


# ####  Using k-fold to run the regression model on the three sets of feature vectors

# In[73]:


num_folds = 5
kf = KFold(n_splits= num_folds, random_state=seed, shuffle = True) # initialise a 5 fold validation
print(kf)


# In[74]:


num_models = 3
cv_df2 = pd.DataFrame(columns = ['description_count', 'title_count', 'combined'],index=range(num_folds)) # creates a dataframe to store the accuracy scores in all the folds

fold = 0
for train_index, test_index in kf.split(list(range(0,len(target)))):
    y_train = [target[i] for i in train_index]
    y_test = [target[i] for i in test_index]
    
    X_train_count, X_test_count = features_cv[train_index], features_cv[test_index]
    cv_df2.loc[fold,'description_count'] = evaluate_reg(features_cv[train_index],features_cv[test_index],y_train,y_test,seed)

    X_train_title, X_test_title = count_title[train_index], count_title[test_index]
    cv_df2.loc[fold,'title_count'] = evaluate_reg(X_train_title, X_test_title,y_train,y_test,seed)
    
    X_train_comb, X_test_comb = combined_count_vectors[train_index], combined_count_vectors[test_index]
    cv_df2.loc[fold,'combined'] = evaluate_reg(X_train_comb, X_test_comb,y_train,y_test,seed)
    
    fold +=1


# In[75]:


cv_df2


# In[76]:


# Plotting the results
plt.figure(figsize=(7, 5))

# Plot each feature representation
plt.plot(cv_df2.index, cv_df2['description_count'], marker='o', label='Description only', color='skyblue')
plt.plot(cv_df2.index, cv_df2['title_count'], marker='o', label='Title only', color='salmon')
plt.plot(cv_df2.index, cv_df2['combined'], marker='o', label='Combined', color='lightgreen')

# Adding titles and labels
plt.title('Model Performance Comparison', fontsize=12)
plt.xlabel('Fold', fontsize=10)
plt.ylabel('Accuracy', fontsize=10)

# Adding legend
plt.legend(fontsize=10)

# Show the plot
plt.grid(True)
plt.xticks(cv_df.index, fontsize=10)
plt.yticks(fontsize=10)
plt.ylim(0, 1)  # Set y-axis range from 0 to 1 for better readability

plt.show()


# From the plot we can observe that performance of description only and the combination of description and title is quite similar. Although title by itself performs worse the difference in accuracy score is not too wide. It even performs better than the two during third iteration. Based on this we can infer that more information does not necessarily give better performance.

# ## Summary
# In this part of the assessment we vectorized the job ads using 3 techniques and used regression model to classify the documents. Additionally, we answered 2 research questions: which model performs better in terms of accuracy and whether more information is better for classification. Comparing the performance of count vectorizer, glove-wiki-gigaword-100 and tf-idf if glove-wiki-gigaword-100, count vectorizer was the clear winner despite not being able to capture semantics. We used the best performing vectorizing technique to answer the second question. We found that for count vectors more information is not necessarily better.

# ## References
# - COSC2820 Advanced Programming for Data Science. (2024). RMIT University
# - How to transform a SciPy sparse matrix to a dictionary. (n.d.). Stack Overflow. Retrieved May 20, 2024, from https://stackoverflow.com/questions/55373331/how-to-transform-a-scipy-sparse-matrix-to-a-dictionary
# 
# - Scipy.Sparse.Dok_matrix.Todok — SciPy v1.13.0 manual. (n.d.). Scipy.org. Retrieved May 20, 2024, from https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.dok_matrix.todok.html
# 
