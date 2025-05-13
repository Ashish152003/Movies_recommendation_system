import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=48fef250c907c9256d7718fb2215056d&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_poster.append(fetch_posters(movie_id))

    return recommended_movies,recommended_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommendor System')

selected_movie_name = st.selectbox(
    "Search Your Movie Here",
    movies['title'].values
)

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columnsrun

    for j in range(5):  # Ensure there's no index out of range error
            with cols[j]:
                st.header(names[j])
                st.image(posters[j])

