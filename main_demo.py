#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 13:55:45 2021

@author: ruoqili
"""


from recom_similarity import book_recom_similarity
from booksampling import get_sampling
from KNN_similarity import user_similarity



if __name__ == '__main__':
    '''
    Sample input_list:
    input_rating = [{'isbn': '0440213525', 'title': 'The Client', 'author': 'John Grisham',
                    'image_url': 'http://images.amazon.com/images/P/0440213525.01.THUMBZZZ.jpg'}, 
    {'isbn': '0385504209', 'title': 'The Da Vinci Code', 'author': 'Dan Brown', 
     'image_url': 'http://images.amazon.com/images/P/0385504209.01.THUMBZZZ.jpg'},
    {'isbn': '0345342968', 'title': 'Fahrenheit 451', 'author': 'RAY BRADBURY', 
     'image_url': 'http://images.amazon.com/images/P/0345342968.01.THUMBZZZ.jpg'}]
    '''
    
    input_rating = {}
    # call the get_sampling() function to randomly get 10 books
    input_list = get_sampling()
  
    for book in input_list:
        rating = input("Rate for "+book['title']+": ")
        input_rating[book['isbn']] = int(rating)
        
    '''
    for title,rating in input_rating.items():
        print(title,rating)
    '''
    
    recom = book_recom_similarity(input_rating)
    result = recom.recommend()
    
    print(result)
    
    recom2 = user_similarity(input_rating)
    
    result2 = recom2.recommend()
    
    print(result2)
        
