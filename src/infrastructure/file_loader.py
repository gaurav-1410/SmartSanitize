import pandas as pd
import streamlit as st
from services.data_validation import FileValidation

class FileHandler:
    def __init__(self):
        self.file_validator = FileValidation()

    def handle_file_upload(self):
        """Handles file upload and validation using Streamlit's uploader"""
        uploaded_file = st.file_uploader("Upload CSV, Excel, or JSON", type=["csv", "xls", "xlsx", "json"])

        if uploaded_file:
            df = self.file_validator.validate_file_format(uploaded_file)

            if df is not None:
                st.session_state.uploaded_df = df
                st.dataframe(df.head(10))  # Display preview
            else:
                st.error("❌ Invalid file format or corrupted file. Please upload a valid CSV, Excel, or JSON.")
