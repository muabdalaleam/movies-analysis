# ==============Importing packeges & reading data==================
import pandas as pd
import numpy as np
import sqlite3
import ast

df = pd.read_csv('../data-mining/raw-data/movies_data.csv')
# ==================================================================


# =======================Cleaning the data==========================
df = df.drop_duplicates(subset='movie_title', keep='first').reset_index(drop=True)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df[df['runtime'] > 10].reset_index(drop= True)


df[['overview', 'tagline']] = df[['overview', 'tagline']] .fillna('')

df = df.astype({'revenue'    : np.uint32,  'budget' : np.uint32,
                'popularity' : np.uint16,  'rating' : np.float32,
                'runtime'    : np.uint16,  'vote_count': np.uint32,
                'movie_id'   : np.uint32})

df['genres']               = df['genres'].apply(ast.literal_eval)
df['production_companies'] = df['production_companies'].apply(ast.literal_eval)


df['release_date']         = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')
# ==================================================================


# ====================Removing the outliers=========================
df_without_outliers = df.copy()

def tucky_method(array: np.array, indecies= True) -> np.array:

    Q3 = np.quantile(array, 0.75)
    Q1 = np.quantile(array, 0.25)
    IQR = Q3 - Q1
    
    upper_range = Q3 + (IQR * 1.5)
    lower_range = Q1 - (IQR * 1.5)
    
    outliers         = [x for x in array if ((x < lower_range) | (x > upper_range))]
    outliers_indexes = np.array(*np.where(np.isin(array, outliers)))
    
    return outliers_indexes

df_without_outliers  = df_without_outliers.drop(tucky_method(df_without_outliers['revenue']))

# df[['revenue', 'budget']] = df[['revenue', 'budget']]   .replace(0, np.nan())
# ==================================================================


# ======================Saving the cleaned data=====================
df.to_parquet('cleaned-data/movies-data.parquet')
df.to_csv('cleaned-data/movies-data.csv', index=False)

df_without_outliers.to_parquet('cleaned-data/movies-data-without-outliers.parquet')
df_without_outliers.to_csv('cleaned-data/movies-data-without-outliers.csv', index=False)


df = df                                   .astype({'genres': str, 'production_companies': str})
df_without_outliers = df_without_outliers .astype({'genres': str, 'production_companies': str})

conn = sqlite3.connect('../database.db')

df                  .to_sql('movies_data', conn, index=False, if_exists= 'replace')
df_without_outliers .to_sql('movies_data_without_outliers', conn, index=False, if_exists= 'replace')

conn.close()
# ==================================================================