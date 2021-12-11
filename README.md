# 95729-Book-Recommendation

- Table of Content
[ToC]
## Design
**Our User Story:** This application is designed for adult users who want to explore more books catering to their tastes. It will be able to recommend new books based on books users have read before to solve the headache of handpicking books.

**Goals and Priorities:** 
- P1:
  * Build a recommendation model with Book-Crossing dataset. Two models will be explored using user-based and item-based collaborative filtering.
  * A web demo that allows users to input book ratings and get their customized readlist.
- P2:
  * Explore other models and try to ensemble to get a better performance.
- P3:
  * Deploy the web app (e.g. on AWS or Azure) and improve UI

**Solid Principles and Design Patterns**
* Solid Principles
We have implemented following solid principles.
(1)	==The Single Responsibility Principle==
A class only have one responsibility and only one reason to change. For example, this project has two class about making prediction. one is **user_similarity**, which do recommendations based on user similarity. The other is **book_recom_similarity**, which recommends according to item similarity. These two classes have different responsibility and thus is separated.
(2)	==Interface Segregation Principle==
A caller need only implement the interfaces it needs to perform a unit of work (UOW). Given the right modality, following ISP should also reduce the impacts of change. 
In this project, we have **multiple interfaces/APIs**. They are segregated in design. For instance, the API to get book list and the API to get the predicted book list are segregated.

* Design Patterns
The project implements ==MVC pattern==. MVC, as an architectural pattern, embodies three parts: Model, View and Controller.
Our **model part holds and process the data**. It directly manages the data and rules of our application. To be more specific, it processes our book dataset and generate user recommendations. 
The **view part displays the resources and serve as a user interface**. In our project, it is the frontend part. 
Our **controller part accepts input and converts it to commands for the model or view**. In this project, the app.py mainly serves as the controller to render presentation of the model in a particular format, responds to the user input, and performs interactions on the data model objects.


## Project Frameworks
A Python machine learning & web application with Flask / Bootstrap / Python. It has basic functions of an online machine learning based recommender system where users can rate randomly generated books. It will then provide personalized recommendation results based on user rating. 

* Technical Stacks:
Flask / Bootstrap / Python / HTML / CSS / JavaScript / Scikit-Learn / Scipy / Pandas


## Start the Project
1. Create a Virtual Environment

* *On macOS and Linux:*
      `python3 -m venv env`
* *On Windows:*
      `py -m venv env`

2. Activate the Virtual Environment
* *On macOS and Linux:*
    `source env/bin/activate`
* *On Windows:*
    `.\env\Scripts\activate`

3. Install dependencies
`pip install -r requirements.txt`

4. Import and Run Flask
At the command line terminal, cd to the project directory and then execute the following command: 
    `flask run`
    
5. Go to http://127.0.0.1:5000/ and try this application.



---
## Data and Model
### Dataset
 We are using two datasets for this recommendation system. 
 * **Bookcrossing Dataset**
     http://www2.informatik.uni-freiburg.de/~cziegler/BX/
     The user-based CF recommendation model uses user-book rating data from this dataset.
 * **Goodbooks Dataset**
 https://www.kaggle.com/alexanderfrosati/goodbooks-10k-updated
     This dataset contains content-specified tags for books, which the content-based recommendation model relies on to calculate the similarity between books. This model uses the data merged by these two datasets.
 
We also preprocessed our datasets to make recommendation more statistically meaningful and avoid over-sparsed calculation.
* **Filter by the users' number of ratings:** Keep only those with more than 10 ratings. 
* **Filter by the books' number of ratiings:** Keep only those that have been rated for more than 50 ratings.
### Model
 * **User-based CF:** We first use KNN model to find 20 users who are most similar to our target user based on their historical rating patterns. We then assign scores to books using adjusted rating and similarity of user-user pairs. Top 10 books with highest scores will be recommended by the model.
![](https://i.imgur.com/LT6HShB.png)


* **Content-based Model**: 
    - **Input:** User - book rating; Book tags data
    - **Calculation：**
    **1. For each book in input:**
    *Step 1：* Use TF_IDF + Cosine Similarity to calculate the similarity score that evaluate how similar a book from the datatset is to this Book A in content.     
    *Step 2：* Calculate the weight according the rate for this Book A. (If the rating is above 5, the weight should be positive and larger with higher rating. Else the weight should be negative and smaller with lower rating)
    *Step 3：* Apply the weight to every book's similarity score to get the final score
    ![](https://i.imgur.com/xewkxEk.png)
    **2. Repeat the steps for every book from the input**
    **3. Sum up the scores for all the books in the dataset and rank descendingly to get top K result**
    ![](https://i.imgur.com/2K2yXbs.png)





---

## Model evaluation
**Root Mean Squared Error**

We will filter out users with >50 ratings and split each user-ratings into train/test dataset in a 7:3 ratio. For each of these users, we will select k similar users who have rated each specific book in the test set. 

**1. Calculate the predicted ratings**
Referring to the following formula, we will first compute the average rating given by the target user. The deviation from similar user's average rating for a book in the test set will also be calculated to mitigate the user rating bias (some users may be more generous/picky about rating). Similarity between target user and similar user will act as a weight component and the weighted scores will be sumed up. The sum product will be divided by the total weight on similarity. In this way, we will be able to predict target user's rating for a specific test book.

![](https://i.imgur.com/6bMmwui.png)
**2. Calculate the RMSE using predicted ratings and true ratings**
Based on the RMSE formula below, we can calculate the error with prediction calculated above and actual rating present in the dataset.
![](https://i.imgur.com/4yTxbhI.png)


## Demo of the Web Interface
* Home Page
![](https://i.imgur.com/P3fYwd0.jpg)

* the User Rating Page
![](https://i.imgur.com/XR7IzX5.png)

* the Recommendation Page
![](https://i.imgur.com/g4yBwfd.jpg)





