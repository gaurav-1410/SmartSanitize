import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from services.quality_analysis import DataSummary, ClassImbalanceAnalyzer

class SummaryPage:
    """
    Displays Data Quality Analysis summary in an interactive dashboard.
    """

    def display(self):
        st.title("📊 Data Quality Analysis")

        if st.session_state.uploaded_df is None:
            st.warning("⚠ No file uploaded. Please upload a dataset first.")
            return

        # Generate Data Summary
        data_summary = DataSummary(st.session_state.uploaded_df)  # Change target column as needed
        report = data_summary.generate_report()
        
        
        # --- 1️⃣ Missing Values Report ---
        st.subheader("🔍 Missing Values Report")
        missing_df = report.get("Missing Values Report")
        if isinstance(missing_df, pd.DataFrame):
            st.dataframe(missing_df)
            # Plot missing values if any exist
            if missing_df["Missing Values"].sum() > 0:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(x=missing_df.index, y=missing_df["Missing Values"], ax=ax, palette="coolwarm", hue=missing_df.index, legend=False)
                plt.xticks(rotation=45)
                plt.ylabel("Count")
                st.pyplot(fig)
        else:
            st.write("No missing values report available.")

        # --- 2️⃣ Duplicate Report ---
        st.subheader("📌 Duplicate Report")
        duplicate_report = report.get("Duplicate Report", {})
        total_duplicates = duplicate_report.get("Total Duplicates", 0)
        st.write(f"**Total Duplicates:** {total_duplicates}")

        # --- 3️⃣ Class Imbalance Report ---
        st.subheader("⚖ Class Imbalance Report")
        target_column = st.text_input("Enter target column for class imbalance analysis:", key="target_column")

        # If the target column is provided, regenerate the DataSummary with that target column
        if target_column:
            # Generate Data Summary with the provided target column
            data_summary = DataSummary(st.session_state.uploaded_df, target_column=target_column)
            imbalance_analyzer= ClassImbalanceAnalyzer
            class_imbalance= imbalance_analyzer.analyze_class_imbalance(st.session_state.uploaded_df,target_column)
            if isinstance(class_imbalance, pd.DataFrame):
                st.dataframe(class_imbalance)
                # Plot class distribution if the DataFrame contains the necessary columns
                if "Class" in class_imbalance.columns and "Percentage" in class_imbalance.columns:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(
                        x=class_imbalance["Class"],
                        y=class_imbalance["Percentage"],
                        palette="muted",
                        ax=ax
                    )
                    plt.ylabel("Percentage")
                    plt.xticks(rotation=90)  
                    st.pyplot(fig)
            else:
                st.write(class_imbalance)
        else:
            st.write("No target column provided for class imbalance analysis.")

        # --- 4️⃣ Anonymized Data Sample ---
        st.subheader("🛡️ Anonymized Data Preview")
        anonymized_sample = report.get("Anonymized Data Sample")
        if isinstance(anonymized_sample, pd.DataFrame):
            st.dataframe(anonymized_sample)
        else:
            st.write("No anonymized data available.")

        # --- 5️⃣ Categorical Value Issues ---
        st.subheader("🔎 Categorical Value Issues")
        cat_value_issues = report.get("Categorical Value Issues")
        if isinstance(cat_value_issues, dict) and cat_value_issues:
            st.write(cat_value_issues)
        else:
            st.write("No categorical value issues detected.")

        # --- 6️⃣ Multicollinearity (VIF) ---
        st.subheader("📏 Multicollinearity - High VIF Features")
        vif_report = report.get("Multicollinearity (High VIF Features)")
        if isinstance(vif_report, pd.DataFrame):
            if not vif_report.empty:
                st.dataframe(vif_report)
            else:
                st.write("No high VIF features detected.")
        elif isinstance(vif_report, dict):
            # In case of error information returned as a dict
            st.write(vif_report.get("Error", "No valid multicollinearity report available."))
        else:
            st.write("No multicollinearity analysis available.")

        # --- 7️⃣ Highly Correlated Features & Correlation Heatmap ---
        st.subheader("🔥 Feature Correlation Heatmap")
        correlated_features = report.get("Highly Correlated Features")
        if isinstance(correlated_features, list) and len(correlated_features) > 0:
            st.write("Highly Correlated Features:", correlated_features)
        else:
            st.write("No highly correlated features detected!")
        # Additionally, display the correlation heatmap for numerical columns
        numerical_df = st.session_state.uploaded_df.select_dtypes(include=['number'])
        if numerical_df.shape[1] > 1:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(numerical_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
            st.pyplot(fig)
        else:
            st.info("Not enough numeric columns for correlation analysis (need at least 2).")

        # --- 8️⃣ Outlier Detection ---
        st.subheader("🚨 Extreme Value Report (Outliers)")
        extreme_values = report.get("Extreme Value Report")
        if isinstance(extreme_values, dict) and extreme_values:
            st.write(extreme_values)
            # Plot boxplots for outlier detection
            numerical_cols = st.session_state.uploaded_df.select_dtypes(include=['number']).columns
            for col in numerical_cols:
                valid_data = st.session_state.uploaded_df[col].dropna()
                if valid_data.shape[0] > 0:  # Ensure non-empty data
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.boxplot(y=valid_data, ax=ax)
                    plt.title(f"Outlier Detection - {col}")
                    st.pyplot(fig)
                else:
                    st.warning(f"Skipping {col}: No valid numeric data available for boxplot.")
        else:
            st.write("No extreme values detected!")


        st.success("✅ Data Quality Analysis Completed!")

