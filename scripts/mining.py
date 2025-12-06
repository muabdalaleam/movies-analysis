import json
import time
from utils import fetch_env, retrying_request

MAX_PAGE = 1 # 20 movies per page
TIMEOUT = 10
MAX_RETRIES = 3
RETRY_WAIT = 0.2 # seconds

api_key = fetch_env('TMBD_API_KEY')
headers = {
    "accept":         "application/json",
    "Authorization": f"Bearer {api_key}"
}

def search_movies(page: int) -> list[str]:
    url = (
        f"https://api.themoviedb.org/3/discover/movie?include_adult=false"
        f"&include_video=false&language=en-US&page={page}&sort_by=vote_count.desc"
    )
    response = retrying_request(url, headers, TIMEOUT, MAX_RETRIES, RETRY_WAIT,
                                raise_on_fail=False)

    if response is None:
        return None

    ids = [movie["id"] for movie in response.json()["results"]]

    return ids

def scrape_movie(id: str) -> dict:
    url    = f"https://api.themoviedb.org/3/movie/{id}"
    response = retrying_request(url, headers, TIMEOUT, MAX_RETRIES, RETRY_WAIT,
                                raise_on_fail=False)

    if response is None:
        return None

    return response.json()


if __name__ == "__main__":
    movies = []
    movie = None

    for i in range(MAX_PAGE):
        movie_ids = search_movies(i+1)
        print(f"Scraping the {i+1}th page of movies from the API with {len(movie_ids)} movies.")

        time.sleep(0.1)

        if not movie_ids or (not movie and i > 0):
            break

        for id in movie_ids:
            movie = scrape_movie(id)
            time.sleep(0.1) # respecting TMDB's api
            movies.append(movie)

            if not movie:
                break

    with open("./data/movies_raw.json", "w") as f:
        json.dump(movies, f)
