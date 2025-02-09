import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from infrastructure.file_loader import FileHandler
from services.preprocessing import DataPreprocessing
from presentation.summary_page import SummaryPage

class UIHandler:
    def __init__(self):
        self.file_handler = FileHandler()
        self.data_preprocessor = DataPreprocessing()

    def display_upload_page(self):
        """Handles file upload UI and processing"""
        st.subheader("📤 Upload Your File")
        self.file_handler.handle_file_upload()  # Calls file upload handler

    def display_data_summary(self):
        """Displays data analysis UI"""
        
        if "uploaded_df" in st.session_state and st.session_state.uploaded_df is not None:
            df = st.session_state.uploaded_df
            summary=SummaryPage()
            summary.display()
            
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")

    def display_preprocessing(self):
        """Displays preprocessing UI"""
        st.subheader("⚙ Data Preprocessing")
        if "uploaded_df" in st.session_state and st.session_state.uploaded_df is not None:
            df = st.session_state.uploaded_df

            selected_methods = self.data_preprocessor.display_null_filling_options(df)

            if st.button("Apply Changes"):
                df = self.data_preprocessor.fill_missing_values(df, selected_methods)
                st.session_state.uploaded_df = df
                st.success("✅ Missing values have been filled successfully!")
                st.dataframe(df.head(10))
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")

    # def display_visualization(self):
    #     """Displays visualization UI"""
    #     st.subheader("📈 Data Visualization")
    #     if "uploaded_df" in st.session_state and st.session_state.uploaded_df is not None:
    #         st.write("Charts and graphs will be displayed here.")
    #     else:
    #         st.warning("⚠ No file uploaded. Please upload a file first.")

    def plot_null_values(self, df):
        """Visualizes missing values"""
        null_counts = df.isnull().sum()
        null_counts = null_counts[null_counts > 0]

        if not null_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=null_counts.index, y=null_counts.values, ax=ax)
            ax.set_title("Missing Values per Column")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.success("✅ No missing values in the dataset!")
