"""
Utility functions for drug overdose death rate analysis.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def parse_demographic_label(stub_label):
    """
    Parse STUB_LABEL into separate demographic components.
    
    Parameters
    ----------
    stub_label : str
        Combined demographic string, e.g., "Male: 25-34 years"
    
    Returns
    -------
    dict
        Dictionary with keys sex, age_group, race_ethnicity
    """
    result = {"sex": None, "age_group": None, "race_ethnicity": None}
    
    if stub_label == "All persons":
        result["sex"] = "All"
        return result
    
    parts = stub_label.split(": ")
    
    if parts[0] in ["Male", "Female"]:
        result["sex"] = parts[0]
        parts = parts[1:]
    
    for part in parts:
        if "years" in part:
            result["age_group"] = part
        else:
            if result["race_ethnicity"] is None:
                result["race_ethnicity"] = part
            else:
                result["race_ethnicity"] += ": " + part
    
    return result


def filter_reliable_estimates(df):
    """
    Remove rows with unreliable estimates (FLAG is not null).
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw data with FLAG column
    
    Returns
    -------
    pd.DataFrame
        Filtered dataframe with only reliable estimates
    """
    return df[df["FLAG"].isna()].copy()


def compute_rate_change(df, start_year, end_year, group_col="STUB_LABEL"):
    """
    Compute absolute and percentage change in death rate between two years.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with YEAR, ESTIMATE, and grouping column
    start_year : int
        Beginning year for comparison
    end_year : int
        Ending year for comparison
    group_col : str
        Column name for demographic grouping
    
    Returns
    -------
    pd.DataFrame
        DataFrame with group, start_rate, end_rate, absolute_change, percent_change
    """
    start_df = df[df["YEAR"] == start_year][[group_col, "ESTIMATE"]].copy()
    start_df.columns = [group_col, "start_rate"]
    
    end_df = df[df["YEAR"] == end_year][[group_col, "ESTIMATE"]].copy()
    end_df.columns = [group_col, "end_rate"]
    
    merged = pd.merge(start_df, end_df, on=group_col)
    merged["absolute_change"] = merged["end_rate"] - merged["start_rate"]
    merged["percent_change"] = (merged["absolute_change"] / merged["start_rate"]) * 100
    
    return merged


def fit_trend_model(df, panel="All drug overdose deaths", demographic="All persons"):
    """
    Fit linear regression of death rate on year.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset with YEAR, ESTIMATE, PANEL, STUB_LABEL columns
    panel : str
        Drug overdose category to filter on
    demographic : str
        STUB_LABEL value to filter on
    
    Returns
    -------
    dict
        Dictionary with slope, intercept, r_squared, predictions, years
    """
    subset = df[(df["PANEL"] == panel) & (df["STUB_LABEL"] == demographic)].copy()
    subset = subset.sort_values("YEAR")
    
    X = subset["YEAR"].values.reshape(-1, 1)
    y = subset["ESTIMATE"].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    predictions = model.predict(X)
    r_squared = model.score(X, y)
    
    return {
        "slope": model.coef_[0],
        "intercept": model.intercept_,
        "r_squared": r_squared,
        "predictions": predictions,
        "years": subset["YEAR"].values
    }