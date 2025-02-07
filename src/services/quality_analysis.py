import pandas as pd

class QualityAnalysis:
    """Handles data quality checks including missing values and recommendations."""

    def __init__(self, df):
        self.df = df

    def recommend_null_handling(self):
        """Recommends best null-filling strategies for each column."""
        recommendations = {}
        
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    # Recommend Mean, Median, or Mode based on distribution
                    if self.df[col].std() < (self.df[col].mean() * 0.1):  # Low variance
                        recommendations[col] = "Mean"
                    else:
                        recommendations[col] = "Median"
                elif pd.api.types.is_string_dtype(self.df[col]):
                    # Recommend Mode or 'Unknown'
                    recommendations[col] = "Mode (Most Frequent)" if self.df[col].nunique() < 10 else "'Unknown'"
                else:
                    recommendations[col] = "Custom Value"
        
        return recommendations
