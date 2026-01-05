# Movies industry analysis

![Line chart change in rating overtime for different movie genres on average (fun-looking chart)](https://github.com/muabdalaleam/movies-analysis/blob/main/assets/screenshot.png?raw=true)

Analysis to the film-making industry using the top-voted movies on TMDB, and sheer curiousity to
find out things like: Most & least profitable genres, Change of average rating throw a movie sequel
& more.

---

# Quick links
- [Analysis notebook](https://nbviewer.org/github/muabdalaleam/movies-analysis/blob/main/notebooks/report.ipynb)
- [Tableau dashboard](https://public.tableau.com/views/MoviesAnalysis_16932561851250/Dashboard1?:language=en-US) *
- [Kaggle dataset](https://www.kaggle.com/datasets/muhammedelsayegh/movies-analysis-dataset) **
- [Analysis PDF report](https://github.com/muabdalaleam/movies-analysis/blob/main/reports/report.pdf)

*: The tabluau dashboard is made long ago on smaller & older data<br>
** : the kaggle dataset is mine for more look here

# Reproducing
If you just want to explore the project the [quick links] would cut it, but if you want to replicate
what I did in the project continue reading this section.<br>
If any of the reproducing steps didn't work for you post an issue describing what went wrong & I
should fix it ASAP.

## Setup
The mining & analysis was done using Python 3.12.11 So i would recommend using a 
[`venv`](https://docs.python.org/3/library/venv.html) with the same Python version though it's
**probably** Ok to use other modern versions.

Firstly clone the repo `git clone https://github.com/muabdalaleam/movies-analysis.git` and move
into it `cd movies-analysis` then create a new `venv` by running `python3 -m venv venv` then
activate it *(depends or your OS)* after you activated the `venv` install the dependicies using
`pip -r install requirements.txt` and that's it.

## Dataset
You can either download my movies dataset from [Kaggle](https://www.kaggle.com/datasets/muhammedelsayegh/movies-analysis-dataset) or mine it yourself again *(might take a
long time)* by following the steps below.<br>

After you have done the setup, you can now run the TMDB data miner but first you should have a
[TMDB API key](https://developer.themoviedb.org/docs/getting-started) and create an enviroment file
in the root of the project `touch ./.env` then write the following in it: 
```TMBD_API_KEY="<YOUR_TMDB_API_KEY>"```
now create the directory where the movies data will be stored `mkdir ./data` now activate your
`venv` & Finally run mining script<br>```python3 ./scripts/mining.py``` now you should have a new
file in the `./data` named `movies_raw.json`<br>

After you have an active `venv` and `./data/movies_raw.json` we are now ready to get the cleaned
data that can be used in the analysis you simply have to run 
```
python3 ./scripts/formatting.py
python3 ./scripts/cleaning.py
```
Now you should have `./data/movies.csv` & `./data/movies_clean.csv`.

## Notebook
Feel free to modify or rerun the report notebook `./notebooks/report.ipynb` just be sure you have
`./data/movies_clean.csv` and a working `venv`.

# Analysis summary
Here is a summary of the cool findings in this project for more look at the 
[Report notebook](https://nbviewer.org/github/muabdalaleam/movies-analysis/blob/main/notebooks/report.ipynb).

- Profitable genres:<br>
History, Science Fiction & Western movies can be really expensive to produce<br>
which highers thier *"budget to revenue"*, Where Horror & Music movies are<br>
relativly cheaper & able to produce a large revenue.
 
- Pobular movies era:<br>
Around 2015 was when most voted movies -on TMDB- were released but fill<br>
drastically after that.

- Genres quality trends:<br>
There was a significant drop in rating across every genre around 1985 that<br>
continued till around 2015 where it was starting to get better again.

- Sequel rating change:<br>
Film sequels tend to diverge to worse & most of them diverged after 4 sequels<br>
to rating of about **~6.5**

### Thanks for looking into my project 💖
