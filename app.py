# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 18:31:45 2023

@author: ariji
"""
import streamlit as st
import pickle
import pandas as pd
import requests
import shutil



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ffdbc06c3dc2f3aa5ff14cf30fb57269&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w185/" + poster_path
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list[1:11]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Movie title',
    (movies['title'].values))

if st.button('Show Recommendation'):
    recommended_movies, recommended_movies_posters = recommend(selected_movie, movies, similarity)
# Display images in a row
    num_columns = 5
    spacing = 5  # Adjust spacing between images and text

    for i in range(0, len(recommended_movies), num_columns):
        cols = st.columns(num_columns)
        for j in range(i, min(i + num_columns, len(recommended_movies))):
            with cols[j - i]:
                st.image(recommended_movies_posters[j], use_column_width=True)
                st.markdown(
    f"<div style='margin-top: 5px; margin-bottom: 5px; margin-left: 0; margin-right: 0;'>{recommended_movies[j]}</div>",
    unsafe_allow_html=True
)
