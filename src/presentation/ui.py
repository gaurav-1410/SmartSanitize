import streamlit as st
from infrastructure.file_loader import handle_file_upload

class UIHandler:
    """Handles the UI rendering for different pages in the app."""
    
    def __init__(self):
        """Initialize any necessary attributes or state."""
        self.uploaded_df = st.session_state.get("uploaded_df", None)

    def display_upload_page(self):
        """Handles file upload UI and processing."""
        st.subheader("📤 Upload Your File")
        self.handle_file_upload()

    def handle_file_upload(self):
        """Handles file upload using the file handler."""
        handle_file_upload()

    def display_data_summary(self):
        """Displays data analysis UI."""
        st.subheader("📊 Data Quality Analysis")
        if self.uploaded_df is not None:
            st.write("This section will include missing value detection, duplicates, and class imbalance checks.")
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")

    def display_preprocessing(self):
        """Displays preprocessing UI."""
        st.subheader("⚙ Data Preprocessing")
        if self.uploaded_df is not None:
            st.write("Options for missing value handling, scaling, and feature selection will be added here.")
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")

    def display_visualization(self):
        """Displays visualization UI."""
        st.subheader("📈 Data Visualization")
        if self.uploaded_df is not None:
            st.write("Charts and graphs will be displayed here.")
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")
