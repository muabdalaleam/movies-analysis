from utils import fetch_env
import requests
import json
# import sqlite3

MAX_PAGE = 500
TIMEOUT = 10

api_key = fetch_env('TMBD_API_KEY')
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# movies_data = []
# 
# for page in range(1, MAX_PAGE + 1):
#     discover_movies_url = (
#         f'https://api.themoviedb.org/3/discover/movie?include_adult=false'
#         f'&include_video=false&language=en-US&page={page}&sort_by=popularity.desc'
#     )
# 
#     discover_movies_response = requests.get(discover_movies_url, headers=HEADERS)
# 
#     for movie in discover_movies_response['results']:
#         movie_id               : str  = movie['id']
#         movie_details_url      : str  = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
#         movie_details_response : dict = requests.get(movie_details_url, headers=HEADERS).json()
# 
#         movie_data = {
#             'movie_id'             : movie_details_response['id'],
#             'movie_title'          : movie_details_response['original_title'],
#             'overview'             : movie_details_response['overview'],
#             'popularity'           : movie_details_response['popularity'],
#             'rating'               : movie_details_response['vote_average'],
#             'tagline'              : movie_details_response['tagline'],
#             'runtime'              : movie_details_response['runtime'],
#             'revenue'              : movie_details_response['revenue'],
#             'release_date'         : movie_details_response['release_date'],
#             'vote_count'           : movie_details_response['vote_count'],
#             'budget'               : movie_details_response['budget'],
#             'genres'               : str([d['name'] for d in movie_details_response['genres']]),
#             'production_companies' : str([d['name'] for d in movie_details_response['production_companies']])
#         }
# 
#         movies_data.append(movie_data)
# 
# 
if __name__ == "__main__":

    print(api_key)
    url = (
        f"https://api.themoviedb.org/3/discover/movie?include_adult=false"
        f"&include_video=false&language=en-US&page={1}&sort_by=vote_count.desc"
    )
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    print(response.json()["results"][0])

    # with sqlite3.connect("./data/movies.db") as con:
    #     conn = sqlite3.connect('../database.db')
    #     movies_data.write_csv('raw-data/movies_data.csv')
    #     movies_data.to_pandas().to_sql('movies_data', con, if_exists='replace', index=False)
