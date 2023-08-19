import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3d2e84a4eecaaedd578da54145b63091&language=en-US'.format(
            movie_id))
    data = response.json()
    # print(data['poster_path'])
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# fetch_poster(65)

movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

#  streamlit website UI

# Lotti files Animation URL JSON
lottie_coding = load_lottieurl("https://lottie.host/4db87bf2-f44c-4a28-99ac-7a0d778d22c2/qsVJNOC1Mc.json")

movies = pd.DataFrame(movies_list)
st.set_page_config(page_title="Movie-Master", page_icon=":sweat_drops:")
with st.container():
    left_column,right_column=st.columns(2)
    with left_column:

        st.subheader('Hi, I am Aryan !!')
        st.write('Welcome To Our Website')
    with right_column:
        st_lottie(lottie_coding,height=150,key="coding")
st.title('Movie Recommender Model')



selected_movie_name = st.selectbox('Search Any movie for the Recommendation ', movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


with st.container():
    st.header('Get in Touch !!')
