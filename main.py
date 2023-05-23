from fastapi import FastAPI
import random
import pickle
import pandas as pd

app = FastAPI()

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    # distances = similarity[movie_index]
    # movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    # for i in movies_list:
    #     movie_id = i[0]
    #     recommended_movies.append(movies.iloc[i[0]].title)
    recommended_movies.append(movies.iloc[movie_index].title)
    return recommended_movies;

movies_dict = pickle.load(open('./model/movie_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('./model/similarity.pkl', 'rb'))
#
@app.get('/')
async def root():
    similar_movies = recommend('Avatar')
    return {
        "Similar": similar_movies
    }