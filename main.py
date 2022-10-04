import book_recommendation as book
import streamlit as st
import requests
from PIL import Image
import pandas as pd

st.header('Book Recommendation System')

user_id = st.text_input('Please enter a user id') 
if user_id:
    user_id = int(user_id)
    if user_id in book.data.user_id.tolist():
        tab1, tab2 = st.tabs(["recommendation", "history"])
        with tab1:
            df = book.recommend_book(user_id)
            st.markdown("Welcome back!")
            if isinstance(df, pd.DataFrame):
                st.write("**recommended books** for user " , user_id)
                col1, col2, col3, col4, col5 = st.columns(5)
                image1 = Image.open(requests.get(df.img_s.tolist()[0], stream=True).raw)
                image2 = Image.open(requests.get(df.img_s.tolist()[1], stream=True).raw)
                image3 = Image.open(requests.get(df.img_s.tolist()[2], stream=True).raw)
                image4 = Image.open(requests.get(df.img_s.tolist()[3], stream=True).raw)
                image5 = Image.open(requests.get(df.img_s.tolist()[4], stream=True).raw)
                col1.image(image1, caption=df.book_title.tolist()[0],  width=100)
                col2.image(image2, caption=df.book_title.tolist()[1],  width=100)
                col3.image(image3, caption=df.book_title.tolist()[2],  width=100)
                col4.image(image4, caption=df.book_title.tolist()[3],  width=100)
                col5.image(image5, caption=df.book_title.tolist()[4],  width=100)
            else:
                genre = st.radio(
                "What kind of book would you like to read?",
                ('Fiction', 'Travel', 'Biography & Autobiography', 'Humor', 'History', 'Religion', 'Social Science', 'Business & Economics', 'Family & Relationships', 'Cooking', 'Poetry', 'Drama', 'Medical', 'Music', 'Gardening'))
                btn = st.button('finish')
                if btn :
                    st.write('You selected ', genre)
                    genre = str(genre)
                    recommend_by_category = book.recommend_by_category(user_id, genre)
                    if isinstance(recommend_by_category, pd.DataFrame):
                        col1, col2, col3, col4, col5 = st.columns(5)
                        image1 = Image.open(requests.get(recommend_by_category.img_s.tolist()[0], stream=True).raw)
                        image2 = Image.open(requests.get(recommend_by_category.img_s.tolist()[1], stream=True).raw)
                        image3 = Image.open(requests.get(recommend_by_category.img_s.tolist()[2], stream=True).raw)
                        image4 = Image.open(requests.get(recommend_by_category.img_s.tolist()[3], stream=True).raw)
                        image5 = Image.open(requests.get(recommend_by_category.img_s.tolist()[4], stream=True).raw)
                        col1.image(image1, caption=recommend_by_category.book_title.tolist()[0],  width=100)
                        col2.image(image2, caption=recommend_by_category.book_title.tolist()[1],  width=100)
                        col3.image(image3, caption=recommend_by_category.book_title.tolist()[2],  width=100)
                        col4.image(image4, caption=recommend_by_category.book_title.tolist()[3],  width=100)
                        col5.image(image5, caption=recommend_by_category.book_title.tolist()[4],  width=100)
                    else:
                        st.write(recommend_by_category)
        with tab2:
            history = book.history(user_id)
            st.write(history)
    else:
        st.markdown('Welcome to book recommendation system!')
        genre = st.radio(
        "What kind of book would you like to read?",
        ('Fiction', 'Travel', 'Biography & Autobiography', 'Humor', 'History', 'Religion', 'Social Science', 'Business & Economics', 'Family & Relationships', 'Cooking', 'Poetry', 'Drama', 'Medical', 'Music', 'Gardening'))
        btn = st.button('finish')
        if btn :
            st.write('You selected ', genre)
            genre = str(genre)
            recommend_by_category = book.recommend_by_category(user_id, genre)
            if isinstance(recommend_by_category, pd.DataFrame):
                col1, col2, col3, col4, col5 = st.columns(5)
                image1 = Image.open(requests.get(recommend_by_category.img_s.tolist()[0], stream=True).raw)
                image2 = Image.open(requests.get(recommend_by_category.img_s.tolist()[1], stream=True).raw)
                image3 = Image.open(requests.get(recommend_by_category.img_s.tolist()[2], stream=True).raw)
                image4 = Image.open(requests.get(recommend_by_category.img_s.tolist()[3], stream=True).raw)
                image5 = Image.open(requests.get(recommend_by_category.img_s.tolist()[4], stream=True).raw)
                col1.image(image1, caption=recommend_by_category.book_title.tolist()[0],  width=100)
                col2.image(image2, caption=recommend_by_category.book_title.tolist()[1],  width=100)
                col3.image(image3, caption=recommend_by_category.book_title.tolist()[2],  width=100)
                col4.image(image4, caption=recommend_by_category.book_title.tolist()[3],  width=100)
                col5.image(image5, caption=recommend_by_category.book_title.tolist()[4],  width=100)
            else:
                st.write(recommend_by_category)

       