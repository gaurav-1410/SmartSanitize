import pandas as pd
import streamlit as st


class DataPreprocessing:
    def recommend_null_filling(self, df):
        """
        Suggests the best method to fill null values for each column.
        If more than 40% of values are missing, it recommends dropping the column.
        """
        recommendations = {}
        total_rows = len(df)

        for col in df.columns:
            null_count = df[col].isnull().sum()
            null_percentage = (null_count / total_rows) * 100

            if null_percentage > 40:
                recommendations[col] = 'Drop Column'  # Suggest dropping the column
            else:
                if df[col].dtype == 'object':
                    recommendations[col] = 'Mode'  # Most frequent category
                elif df[col].dtype in ['int64', 'float64']:
                    if df[col].skew() > 1:
                        recommendations[col] = 'Median'  # Best for skewed data
                    else:
                        recommendations[col] = 'Mean'  # Best for normal distribution
        
        return recommendations

    def display_null_filling_options(self, df):
        """
        Displays UI for selecting null value handling options safely.
        """
        st.subheader("🔍 Null Value Handling Options")

        recommendations = self.recommend_null_filling(df)
        selected_methods = {}

        for col, suggestion in recommendations.items():
            # Default options
            if suggestion == "Drop Column":
                options = ["Drop Column", "Keep & Fill"]
            elif df[col].dtype in ['int64', 'float64']:
                options = ["Mean", "Median", "Mode", "Custom Value", "Drop Column"]
            else:
                options = ["Mode", "Unknown", "Custom Value", "Drop Column"]

            # Safe selection without errors
            try:
                default_index = options.index(suggestion) if suggestion in options else 0
            except ValueError:
                default_index = 0  # Fallback to the first option

            selected_method = st.selectbox(
                f"How should we handle '{col}'? ({df[col].isnull().sum()} missing values)",
                options,
                index=default_index
            )

            # If "Keep & Fill" is selected, provide additional options
            if selected_method == "Keep & Fill":
                if df[col].dtype in ['int64', 'float64']:
                    fill_options = ["Mean", "Median", "Mode", "Custom Value"]
                else:
                    fill_options = ["Mode", "Unknown", "Custom Value"]

                fill_method = st.selectbox(
                    f"Select fill method for '{col}'",
                    fill_options
                )

                if fill_method == "Custom Value":
                    custom_value = st.text_input(f"Enter custom value for {col}:")
                    selected_methods[col] = custom_value
                else:
                    selected_methods[col] = fill_method
            else:
                selected_methods[col] = selected_method
        
        return selected_methods

    def fill_missing_values(self, df, selected_methods):
        """
        Applies selected null value handling options to the dataframe safely.
        """
        columns_to_drop = []

        for col, method in selected_methods.items():
            try:
                if method == "Mean":
                    df[col].fillna(df[col].mean(), inplace=True)
                elif method == "Median":
                    df[col].fillna(df[col].median(), inplace=True)
                elif method == "Mode":
                    df[col].fillna(df[col].mode()[0], inplace=True)
                elif method == "Unknown":
                    df[col].fillna("Unknown", inplace=True)
                elif method == "Drop Column":
                    columns_to_drop.append(col)
                else:
                    df[col].fillna(method, inplace=True)  # Custom value
            except Exception as e:
                st.error(f"⚠ Error filling missing values for '{col}': {str(e)}")

        # Drop columns at the end to avoid modifying dataframe while iterating
        if columns_to_drop:
            df.drop(columns=columns_to_drop, inplace=True)
            st.success(f"✅ Dropped columns: {', '.join(columns_to_drop)}")

        return df
