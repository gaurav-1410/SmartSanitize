import pytest
import pandas as pd
from src.services.preprocessing import handle_missing_values, scale_features

def test_handle_missing_values():
    df = pd.DataFrame({"A": [1, None, 3], "B": [None, 5, 6]})
    
    # Mean imputation
    df_filled = handle_missing_values(df, method="mean")
    assert df_filled.isnull().sum().sum() == 0  # No missing values

    # Drop missing rows
    df_dropped = handle_missing_values(df, method="drop")
    assert df_dropped.shape[0] < df.shape[0]  # Fewer rows

def test_scale_features():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    
    df_scaled = scale_features(df, method="minmax")
    assert df_scaled.min().min() == 0
    assert df_scaled.max().max() == 1
