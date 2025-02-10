import pandas as pd
import numpy as np
import re
from statsmodels.stats.outliers_influence import variance_inflation_factor
from collections import Counter

class MissingValueAnalyzer:
    """Handles missing value analysis."""

    @staticmethod
    def analyze_missing_values(df):
        missing_values = df.isnull().sum()
        missing_percent = (missing_values / len(df)) * 100

        # Detect missing values in categorical columns (empty strings or special characters)
        categorical_columns = df.select_dtypes(exclude=['number']).columns
        for col in categorical_columns:
            empty_string_count = (df[col] == "").sum()
            if empty_string_count > 0:
                missing_values[col] += empty_string_count
                missing_percent[col] = (missing_values[col] / len(df)) * 100

        # Filter only columns with missing values
        missing_data = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_percent})
        missing_data = missing_data[missing_data['Missing Values'] > 0]

        return missing_data



class DuplicateAnalyzer:
    """Handles duplicate row detection."""

    @staticmethod
    def analyze_duplicates(df):
        duplicate_count = df.duplicated().sum()
        return {"Total Duplicates": duplicate_count}

    @staticmethod
    def analyze_near_duplicates(df, text_columns):
        near_duplicates = {}
        for col in text_columns:
            duplicates = df[col].duplicated(keep=False)
            near_duplicates[col] = df[duplicates].shape[0]
        return near_duplicates


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

        # Detect rare categories (<1% of total data)
        rare_categories = {}
        for col in df.select_dtypes(exclude=['number']).columns:
            value_counts = df[col].value_counts(normalize=True)
            rare_categories[col] = value_counts[value_counts < 0.01].index.tolist()
        
        return inconsistent_values, rare_categories


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


class TextColumnHandler:
    """Handles NLP-related checks for text columns."""

    @staticmethod
    def detect_long_tail_text(df, text_columns):
        text_lengths = {}
        for col in text_columns:
            text_lengths[col] = df[col].str.len().describe()

        return text_lengths

    @staticmethod
    def detect_case_variations(df):
        case_issues = {}
        for col in df.select_dtypes(exclude=['number']).columns:
            if df[col].apply(lambda x: isinstance(x, str)).any():
                case_variation = df[col].str.lower().nunique() < df[col].nunique()
                if case_variation:
                    case_issues[col] = True
                else:
                    case_issues[col] = False
        return case_issues


import numpy as np
import pandas as pd
import re

class DataQualityScorer:
    """Computes a comprehensive Data Quality Score based on multiple criteria."""
    
    def __init__(self, df):
        self.df = df
        self.total_rows = len(df)
        self.total_values = df.size
    
    def completeness_score(self):
        missing_values = self.df.isnull().sum().sum() + (self.df == "").sum().sum()
        return max(0, 100 - (missing_values / self.total_values) * 100)
    
    def uniqueness_score(self):
        key_columns = [col for col in self.df.columns if self.df[col].nunique() > 1]  # Ignore columns with single unique value
        duplicate_count = sum(self.df.duplicated(subset=key_columns)) if key_columns else 0
        return max(0, 100 - (duplicate_count / self.total_rows) * 100)
    
    def validity_score(self):
        categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns
        invalid_count = 0
        pattern = re.compile(r'[^a-zA-Z0-9 ]')  # Checks for special characters
        
        for col in categorical_cols:
            invalid_count += self.df[col].astype(str).apply(lambda x: bool(pattern.search(x))).sum()
        
        return max(0, 100 - (invalid_count / self.total_values) * 100)
    
    def accuracy_score(self):
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        outlier_count = 0
        
        for col in numerical_cols:
            Q1, Q3 = self.df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            lower_bound, upper_bound = Q1 - 3 * IQR, Q3 + 3 * IQR  # Adjusted for better outlier detection
            outlier_count += self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col].count()
        
        return max(0, 100 - (outlier_count / self.total_rows) * 100)
    
    def consistency_score(self):
        inconsistent_count = 0
        
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                stripped_values = self.df[col].astype(str).apply(lambda x: x.strip())
                inconsistent_count += (stripped_values.nunique() - self.df[col].nunique())
        
        return max(0, 100 - (inconsistent_count / self.total_rows) * 100)
    
    def timeliness_score(self):
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            latest_date = self.df['date'].max()
            old_records = self.df[self.df['date'] < (latest_date - pd.Timedelta(days=365))]
            return max(0, 100 - (len(old_records) / self.total_rows) * 100)
        return None  # Exclude timeliness if no date column
    
    def calculate_overall_score(self):
        scores = {
            'Completeness': self.completeness_score(),
            'Uniqueness': self.uniqueness_score(),
            'Validity': self.validity_score(),
            'Accuracy': self.accuracy_score(),
            'Consistency': self.consistency_score(),
            'Timeliness': self.timeliness_score()
        }
        
        if scores['Timeliness'] is None:
            scores.pop('Timeliness')
            weights = {'Completeness': 0.33, 'Uniqueness': 0.22, 'Validity': 0.17, 'Accuracy': 0.17, 'Consistency': 0.11}
        else:
            weights = {'Completeness': 0.3, 'Uniqueness': 0.2, 'Validity': 0.15, 'Accuracy': 0.15, 'Consistency': 0.1, 'Timeliness': 0.1}
        
        overall_score = sum(scores[metric] * weights[metric] for metric in scores)
        return round(overall_score, 2), scores





class DataSummary:
    """High-level class that integrates all analysis steps."""

    def __init__(self, df, target_column=None):
        self.df = df
        self.target_column = target_column

    def generate_report(self):
        missing_report = MissingValueAnalyzer.analyze_missing_values(self.df)
        duplicate_report = DuplicateAnalyzer.analyze_duplicates(self.df)

        # Analyzing near-duplicates in text columns
        text_columns = [col for col in self.df.select_dtypes(exclude=['number']).columns if self.df[col].dtype == 'object']
        near_duplicates = DuplicateAnalyzer.analyze_near_duplicates(self.df, text_columns)
        
        anonymized_data = DataAnonymizer.anonymize_data(self.df)
        numerical_cols, categorical_cols = DataTypeHandler.separate_columns(self.df)

        categorical_value_issues, rare_categories = CategoricalValueChecker.check_categorical_values(self.df)
        vif_report = MulticollinearityChecker.calculate_vif(self.df)
        highly_correlated_features = CorrelationHandler.remove_highly_correlated_features(self.df)
        extreme_value_report = OutlierDetector.detect_extreme_values(self.df)
        long_tail_text = TextColumnHandler.detect_long_tail_text(self.df, text_columns)
        case_variations = TextColumnHandler.detect_case_variations(self.df)
        dqs = DataQualityScorer(self.df)
        overall_score, detailed_scores = dqs.calculate_overall_score()


        return {
            "Missing Values Report": missing_report,
            "Duplicate Report": duplicate_report,
            "Near Duplicates in Text Columns": near_duplicates,
            "Anonymized Data Sample": anonymized_data.head(),
            "Numerical Columns": numerical_cols,
            "Categorical Columns": categorical_cols,
            "Categorical Value Issues": categorical_value_issues,
            "Rare Categories (<1%)": rare_categories,
            "Multicollinearity (High VIF Features)": vif_report,
            "Highly Correlated Features": highly_correlated_features,
            "Extreme Value Report": extreme_value_report,
            "Long-Tail Text Distribution": long_tail_text,
            "Case Variations in Text Columns": case_variations,
            "Data Quality Score": [overall_score,detailed_scores]
        }




