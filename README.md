# Movies industry analysis

![Line chart change in rating overtime for different movie genres on average (fun-looking chart)](https://github.com/muabdalaleam/movies-analysis/blob/main/assets/screenshot.png?raw=true)

Analysis to the film-making industry using the top-voted movies on TMDB, and sheer curiousity to find out
things like: Most & least profitable genres, Change of average rating throw a movie sequel & more.

---

# Quick links
- [Analysis notebook]()
- [Tableau dashboard]() *
- [Kaggle dataset]() **
- [Analysis PDF report]()

*: The tabluau dashboard is made long ago on smaller & older data<br>
** : the kaggle dataset is mine for more look here

# Reproducing
If you just want to explore the project the [quick links] would cut it, but if you want to replicate what
I did in the project continue reading this section.

## Setup
The mining & analysis was done using Python 3.12.11 So i would recommend using a [`venv`](https://docs.python.org/3/library/venv.html)
with the same Python version though it's **probably** Ok to use other modern versions.

Firstly clone the repo `git clone https://github.com/muabdalaleam/movies-analysis.git` and move into it `cd movies-analysis`
then create a new `venv` by running `python3 -m venv venv` then activate it *(depends or your OS)* after you activated the `venv`
install the dependicies using `pip -r install requirements.txt` and that's it.

## Dataset
After you have done the setup, you can now run the TMDB data miner but first you should have a [TMDB API key](https://developer.themoviedb.org/docs/getting-started)
and create an enviroment file in the root of the project `touch ./.env` then write the following in it:
```TMBD_API_KEY="<YOUR_TMDB_API_KEY>"```
now create the directory where the movies data will be stored 
