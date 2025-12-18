# Our formatted movies csv has three small problems that needs to be cleaned 
# before starting the analysis & here are they:
# 
# - List values have brackets in the start and end of them.
# - Revenues and budgets can get assigned 0 instead of N/A.
# - Revenue & budget values from TMDB have human insertion errors resulting in
#   outliers.

import pandas as pd
import numpy as np

def remove_brackets(str_list: str) -> str:
    if str_list and isinstance(str_list, str):
        return str_list.replace("\'", "")[1:-1]

    return str_list

def get_z_score(x: float, mean: float, stdev: float) -> float:
    return (x - mean) / stdev


if __name__ == "__main__":
    df = pd.read_csv("./data/movies.csv")

    # Removing the brackets
    df["genres"]               = df["genres"].apply(remove_brackets)
    df["production_countries"] = df["production_countries"].apply(remove_brackets)
    df["production_companies"] = df["production_companies"].apply(remove_brackets)

    # Converting zeros in reveneue & budget to None
    df["revenue"] = df["revenue"].apply(lambda x: None if x == 0 else x)
    df["budget"]  = df["budget"].apply(lambda x:  None if x == 0 else x)

    # Adding z-score columns to track outliers
    revenue_mean   = np.nanmean(df["revenue"])
    revenue_std = np.nanstd(df["revenue"])

    budget_mean   = np.nanmean(df["budget"])
    budget_std = np.nanstd(df["budget"])

    df["revenue_z_score"] = df["revenue"].apply(lambda x: get_z_score(x, revenue_mean, revenue_std))
    df["budget_z_score"]  = df["budget"].apply(lambda x: get_z_score(x, budget_mean, budget_std))

    # Saving the cleaned data
    df.to_csv("./data/movies_clean.csv")
