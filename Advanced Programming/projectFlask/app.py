from flask import Flask, render_template, request, session, redirect
from gensim.models.fasttext import FastText
# import pandas as pd
import pickle
# import os
import numpy as np

# Defining document vector generator
def docvecs(embeddings, docs):
    vecs = np.zeros((len(docs), embeddings.vector_size))
    for i, doc in enumerate(docs):
        valid_keys = [term for term in doc if term in embeddings.key_to_index]
        docvec = np.vstack([embeddings[term] for term in valid_keys])
        docvec = np.sum(docvec, axis=0)
        vecs[i,:] = docvec
    return vecs


app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('home.html',name='Shabnam')

@app.route('/about')
def about():
    return render_template('about.html', page_name='abOUT')

@app.route('/news/<article_name>')
def news(article_name):
    return '<p>This is article {}.</p>'.format(article_name)

@app.route('/hello')
def hello():
    user = request.args.get('user', 'COSC2820')
    return render_template('home.html', name=user)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method=='POST':

        # Read the content
        f_title = request.form['title']
        f_content= request.form['description']

        # tokenize content from the f_content
        tokenized_data = f_content.split(' ')

        # load the model
        bbcFT = FastText.load("bbc.model")
        bbcFT_wv = bbcFT.wv

        # generate vector representation of the tokenized data
        bbcFT_dvs =docvecs(bbcFT_wv, [tokenized_data])

        # load the LR model
        pkl_filename = "bbcFT_LR.pkl"
        with open(pkl_filename, 'rb') as file: # rb is read binary
             model= pickle.load(file)

        # predict the label of tokenized data
        y_pred = model.predict(bbcFT_dvs)
        y_pred = y_pred[0]

        # Set the predicted message 
        predicted_message = 'The category of news is {}.'.format(y_pred)

        return render_template('classify.html', predicted_message=predicted_message, title =f_title, description=f_content)
    else:
        return render_template('classify.html')
