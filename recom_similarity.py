#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 11:22:00 2021

@author: ruoqili
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class book_recom_similarity:
    def __init__(self, user_input):
        self.user_rating = user_input
        self.book_data = pd.read_csv("data/book_tag_data.csv")
        self.book_info = pd.read_csv('data/book_author_url.csv')
        self.tf_corpus = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
        self.tfidf_matrix_corpus = self.tf_corpus.fit_transform(self.book_data['corpus'])
        self.cosine_sim_corpus = linear_kernel(self.tfidf_matrix_corpus, self.tfidf_matrix_corpus)
        self.titles = self.book_data['Book-Title']
        self.indices = pd.Series(self.book_data.index, index=self.book_data['Book-Title'])
        
    def corpus_recommendations(self,title,rating):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim_corpus[idx]))
        
        try:
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]
        except:
            print("An error occured with", str(title))
            return pd.DataFrame(zip(self.titles,np.zeros(len(self.titles))))
        if rating<=5:
            rating=rating-5
        scalar_scores = [i[1]*rating/10 for i in sim_scores]
        book_indices = [i[0] for i in sim_scores]
        return pd.DataFrame(zip(self.titles.iloc[book_indices],scalar_scores))
    
    def recommend(self):
        for i, (isbn, rating) in enumerate(self.user_rating.items()):
            title=self.book_info[self.book_info['ISBN']==isbn]['Book-Title'].values[0]
            
            if i==0:
                recom_pd = self.corpus_recommendations(title,rating)
            else:
                recom_pd=pd.merge(recom_pd, self.corpus_recommendations(title,rating),on=0)
        recom_pd['score']=recom_pd.sum(axis=1)
        sorted_recom = recom_pd.sort_values(by=['score'],ascending=False)[[0]].drop_duplicates(inplace=False,ignore_index=True).head(10)
        sorted_recom.columns=['Book-Title']
        recom_book_df = pd.merge(sorted_recom,self.book_info,on='Book-Title')
        recom_book_df.columns=['title','isbn','author','image_url']
        return recom_book_df.to_dict('records')