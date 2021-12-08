# Importing essential libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import numpy as np
import joblib
from PIL import Image
from recom_similarity import book_recom_similarity
from booksampling import get_sampling
from KNN_similarity import user_similarity


app = Flask(__name__)
app.secret_key = 'O.\x89\xcc\xa0>\x96\xf7\x871\xa2\xe6\x9a\xe4\x14\x91\x0e\xe5)\xd9'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

def get_begin_list():
    # call functions to generate 10 random books
    # begin_list = recommend.recomm()
    '''
    format of begin_list
    [{‘ISBN’: 3647234, ‘title’: ‘Life of Pie’, ‘author’:dhsdw, ‘image_url’: xxxx},
    {‘ISBN’: 3647234, ‘title’: ‘Life of Pie’, ‘author’:dhsdw, ‘image_url’: xxxx}]
    begin_list = [
        {"ISBN": "0195153448", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0002005018", "title": "Clara Callan", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153449", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153450", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153451", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153452", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153453", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153454", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153455", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153456", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"}
    ]
    '''
    begin_list = {}
    # call the get_sampling() function to randomly get 10 books
    begin_list = get_sampling()
    return begin_list

@app.route('/books')
def books():
    begin_list = get_begin_list()
    print(begin_list)
    return render_template('books.html',begin = begin_list)

@app.route('/predict_books', methods=['POST','GET'])
def predict_books():
    # call functions to generate 10 random books
    # begin_list = recommend.recomm()
    '''
    format of begin_list
    [{‘ISBN’: 3647234, ‘title’: ‘Life of Pie’, ‘author’:dhsdw, ‘image_url’: xxxx},
    {‘ISBN’: 3647234, ‘title’: ‘Life of Pie’, ‘author’:dhsdw, ‘image_url’: xxxx}]
    # with demo data
    begin_list = [
        {"ISBN": "0195153448", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0002005018", "title": "Clara Callan", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153449", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153450", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153451", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153452", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153453", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153454", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153455", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"},
        {"ISBN": "0195153456", "title": "Classical Mythology", "author":"dhsdw", "image_url":"http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg"}
    ]
    '''
    begin_list = get_begin_list()
    print(begin_list[0])
    if request.method == 'POST':
        try:
            print("form",request.form)
            respond = request.form.to_dict()
            print("respond",respond)
            print("reach here")
            '''
            rate1 = int(respond[begin_list[2]['isbn']])
            rate2 = int(respond[begin_list[2]['isbn']])
            rate3 = int(respond[begin_list[2]['isbn']])
            rate4 = int(respond[begin_list[3]['isbn']])
            rate5 = int(respond[begin_list[4]['isbn']])
            rate6 = int(respond[begin_list[5]['isbn']])
            rate7 = int(respond[begin_list[6]['isbn']])
            rate8 = int(respond[begin_list[7]['isbn']])
            rate9 = int(respond[begin_list[8]['isbn']])
            rate10 = int(respond[begin_list[9]['isbn']])

            result = [rate1,rate2,rate3,rate4,rate5,rate6,rate7,rate8,rate9,rate10]
            print(result)
            data = defaultdict(int)
            for i in range(len(begin_list)):
                print(begin_list[i]['isbn'])
                data[begin_list[i]['isbn']] = result[i]
            '''
            '''
            format of data: a dictionary
            {[ISBN]:[rating]}
            {‘324234’:3,’328749238’:5,’328748738’:9,’32879238’:6}
            
            # call functions to generate recommendations
            # my_prediction = recommendation.predict(data)

            format of my_prediction
            [{‘ISBN’: 3647234, ‘title’: ‘Life of Pie’, ‘author’:dhsdw, ‘image_url’: xxxx},
            {‘ISBN’: 3647234, ‘title’: ‘Life of Pie’, ‘author’:dhsdw, ‘image_url’: xxxx}]
        
            '''
            for key,value in respond.items():
                respond[key] = int(value)
            print(respond)
            recom = book_recom_similarity(respond)
            item_based_result = recom.recommend()
            print("item",item_based_result)

            recom2 = user_similarity(respond)
            user_based_result = recom2.recommend()
            return render_template('books_result.html', result_item = item_based_result,result_user = user_based_result)
        except ValueError:
            flash(
                'Invalid input. Please fill in the form with appropriate values', 'info')
            return redirect(url_for('books'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
