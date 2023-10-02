# Importing the Libraries
import streamlit as st
import pickle
import pandas as pd
import numpy as np

#---------------------------------------------------------------------------------------------------------------
#Background picture code

img_url = "https://c1.wallpaperflare.com/preview/791/207/698/dark-gloomy-books-pages.jpg"

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://c1.wallpaperflare.com/preview/791/207/698/dark-gloomy-books-pages.jpg");
    background-size: 100%;
    background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
    background-image: url("{img_url}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Importing Pickle Files
df = pickle.load(open('df.pkl', "rb"))
df = pd.DataFrame(df)
pt = pickle.load(open('pivot1.pkl', "rb"))
similarity_scores = pickle.load(open('similarity_scores.pkl', "rb"))
books_list = pickle.load(open('booksdict.pkl', "rb"))
books_list = pd.DataFrame(books_list)
books_list1 = pickle.load(open('booksdict1.pkl', "rb"))
books_list1 = pd.DataFrame(books_list1)
similarity = pickle.load(open('similarity.pkl', "rb"))
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# Basic Code
def recommend_col1(book_name):
    index = np.where(pt.index == book_name)[0][0]
    distances = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    recommended_books = []
    for i in distances:
        df1 = df[df['book_title'] == pt.index[i[0]]]
        book_title = df1.drop_duplicates('book_title')['book_title'].values[0]
        book_author = df1.drop_duplicates('book_title')['book_author'].values[0]
        genres = df1.drop_duplicates('book_title')['Genres'].values[0]
        recommended_books.append(
            f"{len(recommended_books) + 1}) {book_title}\n\nAuthor: {book_author}\n\nGenres: {genres}"
        )
    return recommended_books

def recommend_col2(book):
    index = books_list[books_list['book_title'] == book].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_books = []

    for num, i in enumerate(distances, start=1):
        recommended_books.append(
            f"{num}) {books_list.iloc[i[0]].book_title}\n\nAuthor: {books_list1.iloc[i[0]].book_author}\n\nGenres: {books_list1.iloc[i[0]].Genres}"
        )
    return recommended_books

# Top 10 books
most_read_books=pd.DataFrame(df[['book_title']].value_counts()[:10]).reset_index()[['book_title']]
# By average number of ratings
most_reviewed_books_avg_num = df.groupby("book_title")['num_ratings'].mean().reset_index(name='avg_num_ratings').sort_values( by ='avg_num_ratings',ascending=False ).head(10).reset_index(drop=True)
#Heighest Rated Books
most_reviewed_books_avg =df.groupby('book_title')['avg_rating'].mean().sort_values(ascending=False).reset_index().head(10)
# By City
groupby_city_df = df.groupby(['City', 'book_title'])['num_ratings'].sum().reset_index(name='total_ratings').sort_values(by='total_ratings', ascending=False)
popular_books_city = groupby_city_df.groupby('City').head(1).reset_index(drop=True).head(10)
# By state
groupby_state_df = df.groupby(['State', 'book_title'])['num_ratings'].sum().reset_index(name='total_ratings').sort_values(by='total_ratings', ascending=False)
popular_books_state = groupby_state_df.groupby('State').head(1).reset_index(drop=True).head(10)
# by country
groupby_country_df = df.groupby(['Country', 'book_title'])['num_ratings'].sum().reset_index(name='total_ratings').sort_values(by='total_ratings', ascending=False)
groupby_country_df = groupby_country_df.groupby('Country').head(1).reset_index(drop=True).head(10)
popular_books_country = groupby_country_df.drop(groupby_country_df[groupby_country_df['Country'] == ''].index)

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#Streamlit Code

st.title('Book Recommender System')

# Popularity Based Recommender Systems
if st.button('Most Read Books'):
    st.write(most_read_books)
if st.button('Most Reviewed books (on average number of given ratings)'):
    st.write(most_reviewed_books_avg_num)
if st.button('Most Reviewed books (on average ratings)'):
    st.write(most_reviewed_books_avg)
if st.button('Popular books by location - City'):
    st.write(popular_books_city)
if st.button('Popular books by location - State'):
    st.write(popular_books_state)
if st.button('Popular books by location - Country'):
    st.write(popular_books_country)

#Collaborative filtering based Recommender system
selected_book_name = st.selectbox('Select the Book Name',books_list['book_title'].values)

if st.button('Recommend by Books Similarity'):
    recommendations = recommend_col2(selected_book_name)
    for i in recommendations:
        st.write(i)
if st.button('Recommend by User Preferences (Ratings based)'):
    recommendations = recommend_col1(selected_book_name)
    for i in recommendations:
        st.write(i)
#-----------------------------------------------------------------------------------------------------------------------