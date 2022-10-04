# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:51:59 2022

@author: zehra
"""
import pandas as pd
import numpy as np
from zipfile import ZipFile

with ZipFile('Preprocessed_data.zip', 'r') as file:
    file.extract("Preprocessed_data.csv")

data = pd.read_csv("Preprocessed_data.csv")
data.dropna(inplace=True)
data = data.drop(columns = ['Unnamed: 0', 'location', 'publisher', 'img_l', 'img_m', 'Summary', 'city','state'])

users_age = data[data.age > 0]
users_age = data[data.age < 100]
avg_users_age = users_age['age'].mean()
data['age'].fillna(avg_users_age)
data = data[data.age < 100]
data = data[data.age > 4]
data["age"] = data["age"].values.astype(np.int32)

data = data[data["rating"] != 0]
data["rating"] = data["rating"].values.astype(np.float32)

data = data[data['year_of_publication'] > 0]
data = data[data['year_of_publication'] < 2022]

data.rename(columns = {'Category':'category'}, inplace = True)

avg_rating = data.groupby(['book_title'])['rating'].mean()
avg_rating = avg_rating.reset_index().rename(columns = {'rating': 'avg_rating'})
data = data.merge(avg_rating, on = 'book_title')

df = data[['book_title', 'category', 'img_s']].copy()
df = df.drop_duplicates(subset=['book_title']).reset_index(drop=True)
for i in range(len(df)):
    a = df.iloc[i].category.replace('[', '').replace(']', '').replace("'", '').replace('"', '')          
    df.at[i,'category'] = a   
    
df['rating'] = data['avg_rating']

rating_counts = pd.DataFrame(data["book_title"].value_counts())
rare_books = rating_counts[rating_counts["book_title"] < 5].index
common_books = data[~data["book_title"].isin(rare_books)] 

user_book_df = common_books.pivot_table(index=["user_id"], columns=["book_title"], values="rating")

def history(user_id):
    user_df_wide = data[data.user_id == user_id].reset_index(drop=True)
    for i in range(len(user_df_wide)):
        a = user_df_wide.iloc[i].category.replace('[', '').replace(']', '').replace("'", '').replace('"', '').replace('9', '-').replace('0Islands',  '-').replace('1-00-1---',  '-').replace('1-40-1-4-', '-').replace('11030 - fiction in English - 1-00-1-45 - 60030 - texts', '-').replace('1800-18--', '-').replace('364614153', '-')               
        user_df_wide.at[i,'category'] = a   
    history = user_df_wide[['book_title', 'book_author', 'category', 'rating']].copy().reset_index(drop=True)
    return history

def recommend_by_category(user_id, category):
    category_df = df[df.category == category]
    category_df['rating'] = data['avg_rating']
    
    recommendation_by_category = category_df.sort_values("rating", ascending=False).head(5)
    recommendation_by_category = recommendation_by_category.reset_index(drop=True)
    return recommendation_by_category
    

def recommend_book(user_id):
    user_df = user_book_df[user_book_df.index == user_id]
    books_read = user_df.columns[user_df.notna().any()].tolist()
    books_read_df = user_book_df[books_read]  #pivot table consisting of all users, and books read by the user who has the selected id

    user_df_wide = data[data.user_id == user_df.index.tolist()[0]]
    user_df_wide = user_df_wide.astype({"isbn": str})

    user_book_count = books_read_df.T.notnull().sum().reset_index()  #table showing how many books (same with the user user_id) users read 
    user_book_count.columns = ["userId", "book_count"]

    read_book_th = (user_book_count["book_count"].max()) * 10 / 100  
    users_same_books = user_book_count[user_book_count["book_count"] >= read_book_th]["userId"]   #filters people who read common books with user_id according to the number of books they read

    final_df = pd.concat([books_read_df[books_read_df.index.isin(users_same_books)]])  #creates a table again to correlate these people
 
    corr_df = final_df.T.corr().unstack().sort_values(ascending=False)
    corr_df = pd.DataFrame(corr_df, columns=["corr"])
    corr_df.index = corr_df.index.set_names(['userId1', 'userId2'])
    corr_df = corr_df.reset_index()
    corr_df = corr_df.set_index('userId1')
    corr_df = corr_df[corr_df.index == user_df.index.tolist()[0]]
    corr_df = corr_df[corr_df.userId2 != user_df.index.tolist()[0]]
    corr_df = corr_df.reset_index()  

    top_users = corr_df[(corr_df["corr"] >= 0.8)][["userId2", "corr"]].reset_index(drop=True)
    top_users.rename(columns={"userId2": "user_id"}, inplace=True)

    if top_users.empty:   #to avoid error due to correlation
        return user_id
    else:
        top_users_ratings = top_users.merge(data[["user_id", "isbn", "rating"]], how='inner')
        top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']   #creates a weighted rating according to the correlation between user_id and users
        recommendation_df = top_users_ratings.groupby('isbn').agg({"weighted_rating": "mean"})
        recommendation_df = recommendation_df.reset_index()
        recommendation_df = recommendation_df.astype({"isbn": str})
        isbn_list=[]
        for i in range(len(recommendation_df)):      #eliminates books previously read by user_id
            b_isbn = recommendation_df.iloc[i].isbn
            if b_isbn in user_df_wide.isbn.tolist():
                continue
            else:
                isbn_list.append(b_isbn)            


        recommendation_df = pd.concat([recommendation_df[recommendation_df.isbn.isin(isbn_list)]])
        recommendation_df = recommendation_df.merge(data[["isbn", "book_title", "img_s"]], how='inner').drop_duplicates()


        books_to_be_recommend = recommendation_df.sort_values("weighted_rating", ascending=False).head(5)
        books_to_be_recommend = books_to_be_recommend.reset_index(drop=True)
        return books_to_be_recommend
    
        
   
        
    
