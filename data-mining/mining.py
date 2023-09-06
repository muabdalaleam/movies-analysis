# ==============Importing Packeges & setting constants=============

from google.cloud import bigquery
from itertools import count
from dotenv import load_dotenv

import seaborn as sns
import polars as pl
import numpy as np
import pandas as pd
import requests
import sqlite3
import os

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../credentials.json'
TMBD_API_KEY  : str  = os.getenv('TMBD_API_KEY')
MAX_PAGE      : int  = 500

HEADERS       : dict = {'accept': 'application/json',
                        'Authorization': f'Bearer {TMBD_API_KEY}'}
# =================================================================


# ===============Collecting the data and formatting it=============

movies_data = []

for page in range(1, MAX_PAGE + 1):
    discover_movies_url = (
        f'https://api.themoviedb.org/3/discover/movie?include_adult=false'
        f'&include_video=false&language=en-US&page={page}&sort_by=popularity.desc'
    )

    discover_movies_response = requests.get(discover_movies_url, headers=HEADERS).json()

    for movie in discover_movies_response['results']:
        
        movie_id               : str  = movie['id']
        movie_details_url      : str  = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        movie_details_response : dict = requests.get(movie_details_url, headers=HEADERS).json()

        movie_data = {
            'movie_id'             : movie_details_response['id'],
            'movie_title'          : movie_details_response['original_title'],
            'overview'             : movie_details_response['overview'],
            'popularity'           : movie_details_response['popularity'],
            'rating'               : movie_details_response['vote_average'],
            'tagline'              : movie_details_response['tagline'],
            'runtime'              : movie_details_response['runtime'],
            'revenue'              : movie_details_response['revenue'],
            'release_date'         : movie_details_response['release_date'],
            'vote_count'           : movie_details_response['vote_count'],
            'budget'               : movie_details_response['budget'],
            'genres'               : str([d['name'] for d in movie_details_response['genres']]),
            'production_companies' : str([d['name'] for d in movie_details_response['production_companies']])
        }

        movies_data.append(movie_data)

movies_data = pl.DataFrame(movies_data)
# =================================================================


# ======================Saving the data============================
movies_data.write_csv('raw-data/movies_data.csv')

conn = sqlite3.connect('../database.db')
movies_data.to_pandas().to_sql('movies_data', conn, if_exists='replace', index=False)

conn.close()
# =================================================================
