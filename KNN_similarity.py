# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 22:54:06 2021

@author: Evelyn Wei
"""

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import uuid
  

class user_similarity:
    def __init__(self, user_input):
        self.user_rating = user_input
        self.books = pd.read_csv('book_rating_clean.csv')
        self.book_info = pd.read_csv('book_author_url.csv')
        self. book_pivot = self.books.pivot_table(index='User-ID', columns='ISBN', values="Book-Rating")
        self.book_pivot.fillna(0, inplace=True)
        self.user_id = uuid.uuid4()
        new_row = pd.DataFrame(user_input, index=[self.user_id])
        self.book_pivot = pd.concat([self.book_pivot, new_row]).fillna(0)
        self.book_sparse = csr_matrix(self.book_pivot)
        self.model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute') 
        self.model_knn.fit(self.book_sparse)
        
    def findksimilarusers(self, user_id, k):
        similar_users = []
        similarities = []
        distances, users = self.model_knn.kneighbors(self.book_pivot[-1:].values.reshape(1, -1), n_neighbors = k)
        for i in range(0, len(distances.flatten())):
            similar_users.append(self.book_pivot.index[users.flatten()[i]])
            similarities.append(1-distances.flatten()[i])
        return similar_users, similarities
    

    def computeRating(self):
        similar_users, similarities = self.findksimilarusers(self.user_id, 20)
        all_rating = pd.Series(dtype='float64')
        for i in range(len(similar_users)):
            loc = self.book_pivot.index.get_loc(similar_users[i])
            book = self.book_pivot.iloc[loc, :]
            book_rated = book[book.values > 0]
            # Ratings < 5 will be negatively indexed
            book_rated[book_rated <= 5] = book_rated[book_rated <= 5] - 5
            book_rated_weighted = book_rated / 10
            final_rating = book_rated_weighted * similarities[i]
            all_rating = all_rating.append(final_rating)
        return all_rating
    
    def recommend(self):
        recom_list = []
        total_list = self.computeRating()
        total_index = total_list.index
        user_book_index = self.user_rating.keys()
        intersection = set(total_index).intersection(set(user_book_index))
        # Get rid of books that the user has already read
        new_books = total_list.drop(intersection).sort_values(ascending=False)
        # Remove books with negative ratings
        new_books.drop(labels=new_books[new_books <= 0].index, inplace=True)
        # 10 books to recommend
        recom_books = new_books.iloc[0:10].index
        for i in recom_books:
            book_dict = {}
            book_name = self.books[self.books['ISBN'] == i].drop_duplicates(subset=['ISBN'])['Book-Title'].item()
            book_isbn = self.book_info[self.book_info['Book-Title'] == book_name]['ISBN'].item()
            book_dict['title'] = book_name
            book_dict['isbn'] = book_isbn
            book_dict['author'] = self.book_info[self.book_info['ISBN'] == book_isbn]['Book-Author'].item()
            book_dict['image_url'] = self.book_info[self.book_info['ISBN'] == book_isbn]['Image-URL-S'].item()
            recom_list.append(book_dict)  
        return recom_list
            