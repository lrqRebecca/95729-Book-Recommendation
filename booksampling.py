#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 23:25:45 2021

@author: ruoqili
"""
import pandas as pd

'''
    Randomly sample 10 books from the begining list of books 
'''

def get_sampling():
    book_list = pd.read_csv("data/Begin_book_list.csv")
    return book_list.sample(n=10, replace=False).to_dict('records')