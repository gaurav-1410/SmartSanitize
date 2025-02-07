import pytest
import pandas as pd
from src.services.quality_analysis import detect_missing_values, detect_duplicates

def test_detect_missing_values():
    df = pd.DataFrame({"A": [1, None, 3], "B": [4, None, None]})
    missing_counts = detect_missing_values(df)

    assert missing_counts["A"] == 1
    assert missing_counts["B"] == 2

def test_detect_duplicates():
    df = pd.DataFrame({"A": [1, 2, 2], "B": [3, 4, 4]})
    duplicates = detect_duplicates(df)
    
    assert len(duplicates) == 1  # One duplicate row
