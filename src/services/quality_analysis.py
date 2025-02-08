import pandas as pd
import numpy as np
import re
from statsmodels.stats.outliers_influence import variance_inflation_factor

class MissingValueAnalyzer:
    """Handles missing value analysis."""

    @staticmethod
    def analyze_missing_values(df):
        missing_values = df.isnull().sum()
        missing_percent = (missing_values / len(df)) * 100
        return pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_percent})


class DuplicateAnalyzer:
    """Handles duplicate row detection."""

    @staticmethod
    def analyze_duplicates(df):
        duplicate_count = df.duplicated().sum()
        return {"Total Duplicates": duplicate_count}


class ClassImbalanceAnalyzer:
    """Handles class imbalance detection for categorical target columns."""

    @staticmethod
    def analyze_class_imbalance(df, target_column):
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")

        class_counts = df[target_column].value_counts()
        total_samples = len(df)
        class_percentage = (class_counts / total_samples) * 100

        return pd.DataFrame({'Class': class_counts.index, 'Count': class_counts.values, 'Percentage': class_percentage.values})


class DataAnonymizer:
    """Handles anonymization of sensitive data."""

    @staticmethod
    def anonymize_data(df):
        df_copy = df.copy()

        # Anonymize Email
        email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
        df_copy = df_copy.replace(to_replace=email_pattern, value="*****@*****.com", regex=True)

        # Anonymize Names (Columns containing "Name")
        name_columns = [col for col in df_copy.columns if "name" in col.lower()]
        for col in name_columns:
            df_copy[col] = "Anonymous"

        return df_copy


class DataTypeHandler:
    """Handles numerical and categorical column separation."""

    @staticmethod
    def separate_columns(df):
        numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        return numerical_cols, categorical_cols


class CategoricalValueChecker:
    """Ensures categorical values follow expected formats."""

    @staticmethod
    def check_categorical_values(df):
        inconsistent_values = {}
        for col in df.select_dtypes(exclude=['number']).columns:
            unique_values = df[col].unique()
            cleaned_values = set(value.lower().strip() for value in unique_values if isinstance(value, str))

            if len(cleaned_values) > 10:  # Ignore high cardinality categorical variables
                continue
            
            inconsistent_values[col] = list(cleaned_values)
        return type(inconsistent_values)


class MulticollinearityChecker:
    """Detects multicollinearity using Variance Inflation Factor (VIF)."""

    @staticmethod
    def calculate_vif(df):
        # Select only numerical columns
        numerical_cols = df.select_dtypes(include=['number']).copy()

        if numerical_cols.shape[1] < 2:
            return {"Error": "Not enough numerical columns to check VIF"}

        # Drop any column that has non-numeric values (e.g., object types)
        for col in numerical_cols.columns:
            try:
                numerical_cols[col] = pd.to_numeric(numerical_cols[col], errors='coerce')
            except Exception:
                numerical_cols.drop(columns=[col], inplace=True)

        # Drop any column that still contains NaN values after conversion
        numerical_cols = numerical_cols.dropna(axis=1)

        if numerical_cols.shape[1] < 2:
            return {"Error": "No valid numeric columns for VIF calculation"}

        # Compute VIF
        vif_data = pd.DataFrame()
        vif_data["Feature"] = numerical_cols.columns
        vif_data["VIF"] = [variance_inflation_factor(numerical_cols.values, i) for i in range(len(numerical_cols.columns))]
        
        # Return only features with high VIF
        return vif_data[vif_data["VIF"] > 5]  # Features with VIF > 5 indicate multicollinearity



class CorrelationHandler:
    """Handles feature correlation and removes highly correlated features."""

    @staticmethod
    def remove_highly_correlated_features(df, threshold=0.9):
        # Select numerical columns
        numerical_df = df.select_dtypes(include=['number']).copy()

        # Convert numeric-looking strings to actual numbers
        for col in numerical_df.columns:
            numerical_df[col] = pd.to_numeric(numerical_df[col], errors='coerce')

        # Drop columns that are completely non-numeric (all NaN after conversion)
        numerical_df = numerical_df.dropna(axis=1, how='all')

        if numerical_df.shape[1] < 2:
            return {"Error": "No valid numerical columns for correlation analysis"}

        # Compute correlation matrix
        correlation_matrix = numerical_df.corr().abs()

        # Find highly correlated features
        upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > threshold)]

        return to_drop



class OutlierDetector:
    """Detects extreme values in numerical columns using IQR method."""

    @staticmethod
    def detect_extreme_values(df):
        outlier_report = {}
        for col in df.select_dtypes(include=['number']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]

            if not outliers.empty:
                outlier_report[col] = {"Outlier Count": outliers.count(), "Min Outlier": outliers.min(), "Max Outlier": outliers.max()}

        return outlier_report


class DataSummary:
    """High-level class that integrates all analysis steps."""

    def __init__(self, df, target_column=None):
        self.df = df
        self.target_column = target_column

    def generate_report(self):
        missing_report = MissingValueAnalyzer.analyze_missing_values(self.df)
        duplicate_report = DuplicateAnalyzer.analyze_duplicates(self.df)

        anonymized_data = DataAnonymizer.anonymize_data(self.df)
        numerical_cols, categorical_cols = DataTypeHandler.separate_columns(self.df)

        categorical_value_issues = CategoricalValueChecker.check_categorical_values(self.df)
        vif_report = MulticollinearityChecker.calculate_vif(self.df)
        highly_correlated_features = CorrelationHandler.remove_highly_correlated_features(self.df)
        extreme_value_report = OutlierDetector.detect_extreme_values(self.df)

        return {
            "Missing Values Report": missing_report,
            "Duplicate Report": duplicate_report,
            "Anonymized Data Sample": anonymized_data.head(),
            "Numerical Columns": numerical_cols,
            "Categorical Columns": categorical_cols,
            "Categorical Value Issues": categorical_value_issues,
            "Multicollinearity (High VIF Features)": vif_report,
            "Highly Correlated Features": highly_correlated_features,
            "Extreme Value Report": extreme_value_report
        }


    


