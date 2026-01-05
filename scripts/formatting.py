import json
import csv
from typing import List, Dict

# a dict describing a column name & where to be found within the TMDB json resposnse
MOVIE_DECODER = {
    "id":           "",
    "imdb_id":      "",
    "release_date": "",

    "title":      "original_title",
    "collection": "belongs_to_collection,name",
    "overview":   "",
    "tagline":    "",
    "language":   "original_language",

    "runtime":  "",
    "revenue": "",
    "budget":  "",

    "vote_avg":   "vote_average",
    "vote_count": "vote_count",

    "genres": "genres,name",
    "production_countries": "production_countries,name",
    "production_companies": "production_companies,name",
}

def decode_movie(raw_movie: dict) -> dict:
    clean_movie = dict()

    for col, val_path in MOVIE_DECODER.items():
        if val_path == "":
            try:    clean_movie[col] = raw_movie[col]
            except: clean_movie[col] = None

        elif "," not in val_path:
            try:    clean_movie[col] = raw_movie[val_path]
            except: clean_movie[col] = None

        # Probably this is the dirtiest code I've ever written
        elif "," in val_path:
            val_path_parts = val_path.split(",")
            if len(val_path_parts) > 2:
                raise Exception("decode_movie cann't decode a TMDB movie value with depth more than 2")

            if isinstance(raw_movie[val_path_parts[0]], List):
                clean_movie[col] = []

                for thing in raw_movie[val_path_parts[0]]:
                    if isinstance(thing[val_path_parts[1]], List):
                        clean_movie[col].extend(thing[val_path_parts[1]])
                    else:
                        clean_movie[col].append(thing[val_path_parts[1]])
                continue

            try:    clean_movie[col] = raw_movie[val_path_parts[0]][val_path_parts[1]]
            except: clean_movie[col] = None

    return clean_movie

if __name__ == "__main__":
    with open("./data/movies_raw.json", "r") as f:
        movies = json.load(f)

    with open("./data/movies.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=MOVIE_DECODER.keys())
        writer.writeheader()

        for movie in movies:
            if isinstance(movie, Dict):
                writer.writerow(decode_movie(movie))

