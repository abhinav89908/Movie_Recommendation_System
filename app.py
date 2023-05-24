import streamlit as st
import pickle
import requests
import pandas as pd
import os

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
    #     movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
    recommended_movies.append(movies.iloc[movie_index].title)
    return recommended_movies

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# Get the total number of chunk files
chunk_files = [file for file in os.listdir() if file.startswith('chunk_')]
num_chunks = len(chunk_files)

merged_data = []

for i in range(num_chunks):
    with open(f'chunk_{i}.pkl', 'rb') as file:
        chunk_data = pickle.load(file)
        merged_data.extend(chunk_data)

similarity = merged_data

split_size = 10000  # Number of elements per split
# Split the data into smaller chunks
chunks = [similarity[i:i+split_size] for i in range(0, len(similarity), split_size)]
for i, chunk in enumerate(chunks):
    with open(f'chunk_{i}.pkl', 'wb') as file:
        pickle.dump(chunk, file)



st.title("Movie Recommendation System")
option = st.selectbox(
     'How would you like to be contacted?', (movies['title']))

st.write('You selected:', option)

if st.button("Recommend"):
    lst = recommend(option)
    for i in lst:
        st.write(i)

