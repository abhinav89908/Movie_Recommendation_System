from fastapi import FastAPI
import random
import pickle
import pandas as pd
import os

app = FastAPI()

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
    #     movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
    recommended_movies.append(movies.iloc[movie_index].title)
    return recommended_movies;

movies_dict = pickle.load(open('./model/movie_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
# Get the total number of chunk files
chunk_files = [file for file in os.listdir() if file.startswith('chunk_')]
num_chunks = len(chunk_files)

merged_data = []

for i in range(num_chunks):
    with open(f'chunk_{i}.pkl', 'rb') as file:
        chunk_data = pickle.load(file)
        merged_data.extend(chunk_data)

similarity = merged_data
#
@app.get('/')
async def root():
    similar_movies = recommend('Avatar')
    return {
        "Similar": similar_movies
    }