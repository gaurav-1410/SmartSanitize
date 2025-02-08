import pytest
import pandas as pd
from src.services.quality_analysis import detect_missing_values, detect_duplicates

import pytest
import pandas as pd
from src.services.quality_analysis import (
    MissingValueAnalyzer,
    DuplicateAnalyzer,
    ClassImbalanceAnalyzer,
    DataAnonymizer,
    DataTypeHandler,
    DataSummary,
)

# Sample test dataset
@pytest.fixture
def sample_data():
    data = {
        "Name": ["Alice", "Bob", "Charlie", "Alice", "Eve"],
        "Email": ["alice@example.com", "bob@gmail.com", "charlie@yahoo.com", "alice@example.com", "eve@domain.com"],
        "Age": [25, 30, None, 25, 40],
        "Salary": [50000, None, 70000, 50000, 90000],
        "Gender": ["F", "M", "M", "F", "F"],
        "Target": ["Yes", "No", "Yes", "No", "No"]
    }
    return pd.DataFrame(data)


# ✅ Test for missing values
def test_missing_values(sample_data):
    missing_report = MissingValueAnalyzer.analyze_missing_values(sample_data)
    assert missing_report.loc["Age", "Missing Values"] == 1
    assert missing_report.loc["Salary", "Missing Values"] == 1


# ✅ Test for duplicates
def test_duplicates(sample_data):
    duplicate_report = DuplicateAnalyzer.analyze_duplicates(sample_data)
    assert duplicate_report["Total Duplicates"] == 1  # One duplicate row (Alice appears twice)


# ✅ Test for class imbalance
def test_class_imbalance(sample_data):
    class_report = ClassImbalanceAnalyzer.analyze_class_imbalance(sample_data, "Target")
    assert "Yes" in class_report["Class"].values
    assert "No" in class_report["Class"].values
    assert sum(class_report["Count"]) == len(sample_data)


# ✅ Test for anonymization
def test_anonymization(sample_data):
    anonymized_df = DataAnonymizer.anonymize_data(sample_data)
    
    # Emails should be masked
    assert all(anonymized_df["Email"] == "*****@*****.com")
    
    # Names should be replaced with "Anonymous"
    assert all(anonymized_df["Name"] == "Anonymous")


# ✅ Test for numerical and categorical column separation
def test_column_separation(sample_data):
    numerical_cols, categorical_cols = DataTypeHandler.separate_columns(sample_data)
    
    assert "Age" in numerical_cols
    assert "Salary" in numerical_cols
    assert "Name" in categorical_cols
    assert "Email" in categorical_cols


# ✅ Test DataSummary integration
def test_data_summary(sample_data):
    data_summary = DataSummary(sample_data, target_column="Target")
    report = data_summary.generate_report()

    # Validate missing values
    assert report["Missing Values Report"].loc["Age", "Missing Values"] == 1

    # Validate duplicates
    assert report["Duplicate Report"]["Total Duplicates"] == 1

    # Validate anonymized email
    assert all(report["Anonymized Data Sample"]["Email"] == "*****@*****.com")

    # Validate numerical and categorical columns
    assert "Age" in report["Numerical Columns"]
    assert "Salary" in report["Numerical Columns"]
    assert "Name" in report["Categorical Columns"]
    assert "Email" in report["Categorical Columns"]

