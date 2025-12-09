"""
Tests for analysis_utils module.
"""

import pytest
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "src")
from analysis_utils import (
    parse_demographic_label,
    filter_reliable_estimates,
    compute_rate_change,
    fit_trend_model
)


class TestParseDemographicLabel:
    
    def test_all_persons(self):
        result = parse_demographic_label("All persons")
        assert result["sex"] == "All"
        assert result["age_group"] is None
        assert result["race_ethnicity"] is None
    
    def test_simple_sex(self):
        result = parse_demographic_label("Male")
        assert result["sex"] == "Male"
    
    def test_sex_with_age(self):
        result = parse_demographic_label("Female: 25-34 years")
        assert result["sex"] == "Female"
        assert result["age_group"] == "25-34 years"
        assert result["race_ethnicity"] is None
    
    def test_sex_with_race(self):
        result = parse_demographic_label("Male: White")
        assert result["sex"] == "Male"
        assert result["race_ethnicity"] == "White"
    
    def test_sex_with_complex_race(self):
        result = parse_demographic_label("Male: Not Hispanic or Latino: White")
        assert result["sex"] == "Male"
        assert result["race_ethnicity"] == "Not Hispanic or Latino: White"


class TestFilterReliableEstimates:
    
    def test_removes_flagged_rows(self):
        df = pd.DataFrame({
            "ESTIMATE": [1.0, 2.0, 3.0],
            "FLAG": [None, "unreliable", None]
        })
        result = filter_reliable_estimates(df)
        assert len(result) == 2
        assert 2.0 not in result["ESTIMATE"].values
    
    def test_keeps_all_when_no_flags(self):
        df = pd.DataFrame({
            "ESTIMATE": [1.0, 2.0, 3.0],
            "FLAG": [None, None, None]
        })
        result = filter_reliable_estimates(df)
        assert len(result) == 3


class TestComputeRateChange:
    
    def test_basic_change(self):
        df = pd.DataFrame({
            "YEAR": [1999, 1999, 2017, 2017],
            "STUB_LABEL": ["A", "B", "A", "B"],
            "ESTIMATE": [10.0, 20.0, 15.0, 30.0]
        })
        result = compute_rate_change(df, 1999, 2017)
        row_a = result[result["STUB_LABEL"] == "A"].iloc[0]
        assert row_a["start_rate"] == 10.0
        assert row_a["end_rate"] == 15.0
        assert row_a["absolute_change"] == 5.0
        assert row_a["percent_change"] == 50.0


class TestFitTrendModel:
    
    def test_returns_expected_keys(self):
        df = pd.DataFrame({
            "YEAR": [1999, 2000, 2001, 2002],
            "PANEL": ["All drug overdose deaths"] * 4,
            "STUB_LABEL": ["All persons"] * 4,
            "ESTIMATE": [6.0, 7.0, 8.0, 9.0]
        })
        result = fit_trend_model(df)
        assert "slope" in result
        assert "intercept" in result
        assert "r_squared" in result
        assert "predictions" in result
        assert "years" in result
    
    def test_perfect_linear_trend(self):
        df = pd.DataFrame({
            "YEAR": [2000, 2001, 2002, 2003],
            "PANEL": ["All drug overdose deaths"] * 4,
            "STUB_LABEL": ["All persons"] * 4,
            "ESTIMATE": [10.0, 11.0, 12.0, 13.0]
        })
        result = fit_trend_model(df)
        assert abs(result["slope"] - 1.0) < 0.01
        assert abs(result["r_squared"] - 1.0) < 0.01