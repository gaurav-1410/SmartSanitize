import pandas as pd
import streamlit as st
from services.data_validation import FileValidation


class FileHandler:
    """
    Handles file uploads and validation.
    """

    def __init__(self):
        self.validator = FileValidation()

    def load_file(self, uploaded_file):
        """
        Loads a file (CSV, Excel, JSON) and validates it.
        """
        if uploaded_file is None:
            return None

        df = self.validator.validate_file_format(uploaded_file)  # Validate and load file
        return df

    def handle_file_upload(self):
        """
        Handles file upload and validation using Streamlit's uploader.
        """
        uploaded_file = st.file_uploader("Upload CSV, Excel, or JSON", type=["csv", "xls", "xlsx", "json"])

        if uploaded_file:
            df = self.load_file(uploaded_file)  # Loads and validates file

            if df is not None:
                st.session_state.uploaded_df = df
                st.dataframe(st.session_state.uploaded_df.head(10))  # Display preview
            else:
                st.error("❌ Invalid file format or corrupted file. Please upload a valid CSV, Excel, or JSON.")
