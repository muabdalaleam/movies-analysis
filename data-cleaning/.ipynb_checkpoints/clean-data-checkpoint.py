# ==============Importing packeges & reading data==================
import pandas as pd
import numpy as np
import sqlite3
import ast

conn = sqlite3.connect("../database.db")
df = pd.read_sql_query("SELECT * from `movies_data`", conn)

conn.close()
# ==================================================================


# =======================Cleaning the data==========================
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df[['overview', 'tagline']] .fillna('')
df[['revenue', 'budget']]   .replace(0, np.nan)

df = df.astype({'revenue'    : np.uint32,  'budget' : np.uint32,
                'popularity' : np.float16, 'rating' : np.float16,
                'runtime'    : np.uint16,  'vote_count': np.uint32})

df['genres']               = df['genres'].apply(ast.literal_eval)
df['production_companies'] = df['production_companies'].apply(ast.literal_eval)


df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')
# ==================================================================


# ====================Removing the outliers=========================
df_without_outliers = df.copy()

def tucky_method(array: np.array, indecies= True) -> np.array:

    Q3 = np.quantile(array, 0.75)
    Q1 = np.quantile(array, 0.25)
    IQR = Q3 - Q1
    
    upper_range = Q3 + (IQR * 1.5)
    lower_range = Q1 - (IQR * 1.5)
    
    outliers_indexes = [x for x in array if ((x < lower_range) | (x > upper_range))]
    print(f"Found {len(outliers_indexes)} outliers from {len(outliers_indexes)} length series!")
    
    return outliers_indexes

outliers_indexes     = tucky_method(df_without_outliers['revenue'].to_numpy())
outliers             = np.array(*np.where(np.isin(df_without_outliers['revenue'], outliers_indexes)))

df_without_outliers  = df_without_outliers.drop(outliers)
# ==================================================================


# ======================Saving the cleaned data=====================
df.to_pickle('cleaned-data/movies-data.pkl')
df.to_csv('cleaned-data/movies-data.csv')

df_without_outliers.to_pickle('cleaned-data/movies-data-without-outliers.pkl')
df_without_outliers.to_csv('cleaned-data/movies-data-without-outliers.csv')


df = df                                   .astype({'genres': str, 'production_companies': str})
df_without_outliers = df_without_outliers .astype({'genres': str, 'production_companies': str})

conn = sqlite3.connect('../database.db')

df                  .to_sql('movies_data', conn, index=False, if_exists= 'replace')
df_without_outliers .to_sql('movies_data_without_outliers', conn, index=False, if_exists= 'replace')

conn.close()
# ==================================================================