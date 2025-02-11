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
            summary = SummaryPage()
            summary.display()
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")

    def display_preprocessing(self):
        """Displays preprocessing UI with column management and missing value handling"""
        st.subheader("⚙ Data Preprocessing")

        if "uploaded_df" in st.session_state and st.session_state.uploaded_df is not None:
            df = st.session_state.uploaded_df

            # Column Management: Rename or Delete Columns
            st.subheader("🛠 Column Management")
            df = self.data_preprocessor.modify_columns(df)
            st.session_state.uploaded_df = df  # Update session state after modification

            # Null Value Handling
            # st.subheader("🔍 Null Value Handling")
            selected_methods = self.data_preprocessor.display_null_filling_options(df)

            if selected_methods and st.button("Apply Changes"):
                df = self.data_preprocessor.fill_missing_values(df, selected_methods)
                st.session_state.uploaded_df = df  # Update session state
                st.success("✅ Missing values have been handled successfully!")

            # Show updated dataframe preview
            st.subheader("📌 Updated Dataset Preview")
            st.dataframe(df.head(10))

        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")

    def plot_null_values(self, df):
        """Visualizes missing values"""
        null_counts = df.isnull().sum()
        null_counts = null_counts[null_counts > 0]  # Show only columns with missing values

        if not null_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=null_counts.index, y=null_counts.values, ax=ax)
            ax.set_title("Missing Values per Column")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.success("✅ No missing values in the dataset!")
