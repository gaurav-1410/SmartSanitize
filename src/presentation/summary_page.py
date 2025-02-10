# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np
# from services.quality_analysis import DataSummary, ClassImbalanceAnalyzer

# class SummaryPage:
#     """
#     Displays Data Quality Analysis summary in an interactive dashboard.
#     """

#     def display(self):
#         if st.session_state.uploaded_df is None:
#             st.warning("⚠ No file uploaded. Please upload a dataset first.")
#             return

#         # Generate Data Summary
#         data_summary = DataSummary(st.session_state.uploaded_df)  # Change target column as needed
#         report = data_summary.generate_report()
        
#         # Save the report to session state
#         st.session_state.data_summary_report = report
        
#         # --- 1️⃣ Missing Values Report ---
#         st.subheader("🔍 Missing Values Report")
#         missing_df = report.get("Missing Values Report")
#         if missing_df["Missing Values"].sum() > 0:
#             if isinstance(missing_df, pd.DataFrame):
#                     st.dataframe(missing_df)
#                     fig = px.bar(missing_df, x=missing_df.index, y="Missing Values", title="Missing Values Count", color="Missing Values")
#                     fig.update_layout(height=600, width=800)
#                     st.plotly_chart(fig)
#         else:
#             st.write("No missing values report available.")

#         # --- 2️⃣ Duplicate Report ---
#         st.subheader("📌 Duplicate Report")
#         duplicate_report = report.get("Duplicate Report", {})
#         total_duplicates = duplicate_report.get("Total Duplicates", 0)
#         st.write(f"**Total Duplicates:** {total_duplicates}")

#         # --- 3️⃣ Class Imbalance Report ---
#         st.subheader("⚖ Class Imbalance Report")
#         target_column = st.text_input("Enter target column for class imbalance analysis:", key="target_column")
        
#         if target_column:
#             data_summary = DataSummary(st.session_state.uploaded_df, target_column=target_column)
#             imbalance_analyzer = ClassImbalanceAnalyzer()
#             class_imbalance = imbalance_analyzer.analyze_class_imbalance(st.session_state.uploaded_df, target_column)
#             st.session_state.class_imabalance= class_imbalance
#             if isinstance(class_imbalance, pd.DataFrame):
#                 st.dataframe(class_imbalance)
#                 if "Class" in class_imbalance.columns and "Percentage" in class_imbalance.columns:
#                     fig = px.bar(class_imbalance, x="Class", y="Percentage", title="Class Distribution", color="Percentage")
#                     fig.update_layout(height=600, width=800)
#                     st.plotly_chart(fig)
#             else:
#                 st.write(class_imbalance)
#         else:
#             st.write("No target column provided for class imbalance analysis.")

#         # --- 4️⃣ Anonymized Data Sample ---
#         st.subheader("🛡️ Anonymized Data Preview")
#         anonymized_sample = report.get("Anonymized Data Sample")
#         if isinstance(anonymized_sample, pd.DataFrame):
#             st.dataframe(anonymized_sample)
#         else:
#             st.write("No anonymized data available.")

#         # --- 5️⃣ Categorical Value Issues ---
#         st.subheader("🔎 Categorical Value Issues")
#         cat_value_issues = report.get("Categorical Value Issues")
#         if isinstance(cat_value_issues, dict) and cat_value_issues:
#             st.write(cat_value_issues)
#         else:
#             st.write("No categorical value issues detected.")

#         # --- 6️⃣ Multicollinearity (VIF) ---
#         st.subheader("📏 Multicollinearity - High VIF Features")
#         vif_report = report.get("Multicollinearity (High VIF Features)")
#         if isinstance(vif_report, pd.DataFrame):
#             if not vif_report.empty:
#                 st.dataframe(vif_report)
#             else:
#                 st.write("No high VIF features detected.")
#         elif isinstance(vif_report, dict):
#             st.write(vif_report.get("Error", "No valid multicollinearity report available."))
#         else:
#             st.write("No multicollinearity analysis available.")

#         # --- 7️⃣ Highly Correlated Features & Correlation Heatmap ---
#         st.subheader("🔥 Feature Correlation Heatmap")
#         correlated_features = report.get("Highly Correlated Features")
#         if isinstance(correlated_features, list) and len(correlated_features) > 0:
#             st.write("Highly Correlated Features:", correlated_features)
#         else:
#             st.write("No highly correlated features detected!")
#         numerical_df = st.session_state.uploaded_df.select_dtypes(include=['number'])
#         if not numerical_df.empty:
#             corr_matrix = numerical_df.corr()
#             fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='blues', title='Correlation Heatmap')
#             fig.update_layout(height=800, width=1000)
#             st.plotly_chart(fig)
#         else:
#             st.info("No numeric columns available for correlation analysis.")

#         # --- 8️⃣ Outlier Detection ---
#         st.subheader("🚨 Extreme Value Report (Outliers)")
#         extreme_values = report.get("Extreme Value Report")
#         if isinstance(extreme_values, dict) and extreme_values:
#             st.write(extreme_values)
#             numerical_cols = st.session_state.uploaded_df.select_dtypes(include=['number']).columns
#             for col in numerical_cols:
#                 fig = px.box(st.session_state.uploaded_df, y=col, title=f"Outlier Detection - {col}")
#                 fig.update_layout(height=600, width=800)
#                 st.plotly_chart(fig)
#         else:
#             st.write("No extreme values detected!") 

#         st.success("✅ Data Quality Analysis Completed!")

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from services.quality_analysis import DataSummary, ClassImbalanceAnalyzer

class SummaryPage:
    """
    Displays Data Quality Analysis summary in an interactive dashboard.
    """

    def display(self):
        if st.session_state.uploaded_df is None:
            st.warning("⚠ No file uploaded. Please upload a dataset first.")
            return

        # Generate Data Summary
        data_summary = DataSummary(st.session_state.uploaded_df)  
        report = data_summary.generate_report()

        # Store the report in session state
        st.session_state.data_summary_report = report

        # --- 1️⃣ Missing Values Report ---
        self.display_missing_values(report)

        # --- 2️⃣ Duplicate Report ---
        self.display_duplicates(report)

        # --- 3️⃣ Near Duplicates in Text Columns ---
        self.display_near_duplicates(report)

        # --- 4️⃣ Class Imbalance Report ---
        self.display_class_imbalance(report)

        # --- 5️⃣ Anonymized Data Sample ---
        self.display_anonymized_data(report)

        # --- 6️⃣ Numerical & Categorical Columns ---
        self.display_column_types(report)

        # --- 7️⃣ Categorical Value Issues & Rare Categories ---
        self.display_categorical_issues(report)

        # --- 8️⃣ Multicollinearity (VIF) ---
        self.display_multicollinearity(report)

        # --- 9️⃣ Highly Correlated Features & Heatmap ---
        self.display_correlation_heatmap(report)

        # --- 🔟 Outlier Detection ---
        self.display_outliers(report)

        # --- 1️⃣1️⃣ Long-Tail Text Distribution ---
        self.display_long_tail_text(report)

        # --- 1️⃣2️⃣ Case Variations in Text Columns ---
        self.display_case_variations(report)

        # --- 1️⃣3️⃣ Overall Data Quality Score ---
        self.display_quality_score(report)

        st.success("✅ Data Quality Analysis Completed!")

    def display_missing_values(self, report):
        """ Display missing values report """
        st.subheader("🔍 Missing Values Report")
        missing_df = report.get("Missing Values Report")
        if missing_df is not None and isinstance(missing_df, pd.DataFrame) and missing_df["Missing Values"].sum() > 0:
            st.dataframe(missing_df)
            fig = px.bar(missing_df, x=missing_df.index, y="Missing Values", title="Missing Values Count", color="Missing Values")
            st.plotly_chart(fig)
        else:
            st.write("No missing values detected.")

    def display_duplicates(self, report):
        """ Display duplicate report """
        st.subheader("📌 Duplicate Report")
        duplicate_report = report.get("Duplicate Report", {})
        total_duplicates = duplicate_report.get("Total Duplicates", 0)
        st.write(f"**Total Duplicates:** {total_duplicates}")

    def display_near_duplicates(self, report):
        """ Display near duplicates in text columns """
        st.subheader("🔄 Near Duplicates in Text Columns")
        near_duplicates = report.get("Near Duplicates in Text Columns")
        if near_duplicates:
            st.write(near_duplicates)
        else:
            st.write("No near duplicates found.")

    def display_class_imbalance(self, report):
        """Display class imbalance report only after user selects a column."""
        st.subheader("⚖ Class Imbalance Report")

        # Let user select a column but do not run analysis until selected
        target_column = st.selectbox("Select target column for class imbalance analysis:", 
                                    ["Select a column"] + list(st.session_state.uploaded_df.columns), 
                                    index=0)

        if target_column != "Select a column":
            imbalance_analyzer = ClassImbalanceAnalyzer()
            try:
                class_imbalance = imbalance_analyzer.analyze_class_imbalance(st.session_state.uploaded_df, target_column)
                st.session_state.class_imbalance = class_imbalance

                # Display the DataFrame
                st.dataframe(class_imbalance)

                # Display bar chart only if valid data is present
                if not class_imbalance.empty:
                    fig = px.bar(class_imbalance, x="Class", y="Percentage", title="Class Distribution", color="Percentage")
                    st.plotly_chart(fig)
                else:
                    st.write("No class imbalance detected.")

            except ValueError as e:
                st.error(f"❌ {e}")

        else:
            st.info("ℹ Please select a target column to analyze class imbalance.")

    def display_anonymized_data(self, report):
        """ Display anonymized data sample """
        st.subheader("🛡️ Anonymized Data Preview")
        anonymized_sample = report.get("Anonymized Data Sample")
        if isinstance(anonymized_sample, pd.DataFrame):
            st.dataframe(anonymized_sample)
        else:
            st.write("No anonymized data available.")

    def display_column_types(self, report):
        """ Display numerical and categorical column information """
        st.subheader("📊 Column Types")
        numerical_cols = report.get("Numerical Columns")
        categorical_cols = report.get("Categorical Columns")
        st.write(f"**Numerical Columns:** {numerical_cols}")
        st.write(f"**Categorical Columns:** {categorical_cols}")

    def display_categorical_issues(self, report):
        """ Display categorical value issues and rare categories """
        st.subheader("🔎 Categorical Value Issues")
        cat_value_issues = report.get("Categorical Value Issues")
        rare_categories = report.get("Rare Categories (<1%)")
        st.write(cat_value_issues or "No categorical value issues detected.")
        st.write(rare_categories or "No rare categories detected.")

    def display_multicollinearity(self, report):
        """ Display multicollinearity report """
        st.subheader("📏 Multicollinearity - High VIF Features")
        vif_report = report.get("Multicollinearity (High VIF Features)")
        if isinstance(vif_report, pd.DataFrame) and not vif_report.empty:
            st.dataframe(vif_report)
        else:
            st.write("No high VIF features detected.")

    def display_correlation_heatmap(self, report):
        """ Display correlation heatmap """
        st.subheader("🔥 Feature Correlation Heatmap")
        correlated_features = report.get("Highly Correlated Features", [])
        if correlated_features:
            st.write("Highly Correlated Features:", correlated_features)
        numerical_df = st.session_state.uploaded_df.select_dtypes(include=['number'])
        if not numerical_df.empty:
            fig = px.imshow(numerical_df.corr(), text_auto=True, color_continuous_scale='blues', title='Correlation Heatmap')
            st.plotly_chart(fig)
        else:
            st.info("No numeric columns available for correlation analysis.")

    def display_outliers(self, report):
        """ Display extreme value report """
        st.subheader("🚨 Outlier Detection")
        extreme_values = report.get("Extreme Value Report")
        if extreme_values:
            st.write(extreme_values)
            for col in st.session_state.uploaded_df.select_dtypes(include=['number']).columns:
                fig = px.box(st.session_state.uploaded_df, y=col, title=f"Outlier Detection - {col}")
                st.plotly_chart(fig)
        else:
            st.write("No extreme values detected.")

    def display_long_tail_text(self, report):
        """ Display long-tail text distribution """
        st.subheader("📜 Long-Tail Text Distribution")
        long_tail_text = report.get("Long-Tail Text Distribution")
        st.write(long_tail_text or "No long-tail text distribution detected.")

    def display_case_variations(self, report):
        """ Display case variations in text columns """
        st.subheader("🔡 Case Variations in Text Columns")
        case_variations = report.get("Case Variations in Text Columns")
        st.write(case_variations or "No case variations detected.")

    def display_quality_score(self, report):
        """ Display data quality score """
        st.subheader("🎯 Data Quality Score")
        data_quality_score = report.get("Data Quality Score")
        st.write(data_quality_score or "No quality score available.")
