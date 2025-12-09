import json
import csv

# a dict describing a value & where to be found within the TMDB json resposnse
TMDB_MOVIE_DECODER = {
    "id":           "id",
    "release_date": "",

    "title":      None,
    "collection": None,
    "overview":   None,
    "tagline":    None,
    "language":   None,

    "runtime":  None,
    "revenue": None,
    "budget":  None,

    "vote_avg":   None,
    "vote_count": None,

    "genres": [],
    "countries": [],
    "production_companies": [],
}

if __name__ == "__main__":
    with open("./data/movies_raw.json", "r") as f:
        movies = json.load(f)

    print(movies[67])

    # with open("./data/movies_clean.csv", "w") as f:
    #     writer = csv.DictWriter(f, fieldnames=movie_template.keys())
    #     writer.writeheader()

    #     for movie in movies:
    #         clean_movie = movie_template

    #         writer.writerow(movie_template)

