# ==============Importing Packeges & setting constants=============

# from google.cloud import bigquery
from itertools import count
from dotenv import load_dotenv

import seaborn as sns
import pandas as pd
import numpy as np
import requests
import os

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../credentials.json'
TMBD_API_KEY  : str  = os.getenv('TMBD_API_KEY')
MAX_PAGE      : int  = 2

HEADERS       : dict = {'accept': 'application/json',
                        'Authorization': f'Bearer {TMBD_API_KEY}'}
# =================================================================


# ===============Collecting the data and formatting it=============
movie_ids            : list = []
movies_titles        : list = []
overviews            : list = []
popularities         : list = []
ratings              : list = []
taglines             : list = []
runtimes             : list = []
revenues             : list = []
release_dates        : list = []
vote_counts          : list = []
budgets              : list = []
genres               : list = []
production_companies : list = []
    
movies_ids = []

for i in count(0):

    page : int = i + 1
    if page > MAX_PAGE:
        break

    discover_movies_url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false' + \
                        '&include_video=false&language=en-US&page={page}&sort_by=popularity.desc'
    
    discover_movies_response = requests.get(discover_movies_url, headers= HEADERS).json()

    for movie in discover_movies_response['results']:
        movies_ids.append(movie['id'])


for movie_id in movies_ids:

    movie_details_url      = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    movie_details_response = requests.get(movie_details_url, headers= HEADERS).json()
    
    movie_ids     .append(movie_details_response['id'])
    movies_titles .append(movie_details_response['original_title'])
    overviews     .append(movie_details_response['overview'])
    popularities  .append(movie_details_response['popularity'])
    ratings       .append(movie_details_response['vote_average'])
    taglines      .append(movie_details_response['tagline'])
    runtimes      .append(movie_details_response['runtime'])
    revenues      .append(movie_details_response['revenue'])
    release_dates .append(movie_details_response['release_date'])
    vote_counts   .append(movie_details_response['vote_count'])
    budgets       .append(movie_details_response['budget'])
    
    genres                .append([d['name'] for d in movie_details_response['genres']])
    production_companies  .append([d['name'] for d in movie_details_response['production_companies']])


movies_data  =  pd.DataFrame({'movie_id' : movie_ids,
                'movie_title'            : movies_titles,
                'overview'               : overviews,
                'popularity'             : popularities ,
                'rating'                 : ratings,
                'tagline'                : taglines,
                'runtime'                : runtimes,
                'revenue'                : revenues,
                'release_data'           : release_dates,
                'vote_count'             : vote_counts,
                'budget'                 : budgets,
                'genres'                 : genres,
                'production_companies'   : production_companies})
# =================================================================


# ==============Saving the data & uploading it=====================
dataset_id       :str = 'movies-analysis-db'
project_id       :str = 'data-jobs-analysis-db'

table_id   = f'{project_id}.{dataset_id}.{table_name}'

job_config = bigquery.LoadJobConfig(write_disposition= 'WRITE_TRUNCATE')
job        = client.load_table_from_dataframe(df, table_id, job_config=job_config)

job.result()
# =================================================================

print(movies_data.head())
