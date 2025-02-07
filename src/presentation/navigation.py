import streamlit as st
from presentation.upload_page import UploadPage
from presentation.summary_page import SummaryPage
from presentation.preprocessing_page import PreprocessingPage
from presentation.visualization_page import VisualizationPage


class Navigation:
    """
    Manages the navigation between different pages.
    """

    def __init__(self):
        self.upload_page = UploadPage()
        self.summary_page = SummaryPage()
        self.preprocessing_page = PreprocessingPage()
        self.visualization_page = VisualizationPage()

    def display_page(self):
        """
        Displays the selected page based on sidebar navigation.
        """
        st.sidebar.header("Navigation")
        page = st.sidebar.radio(
            "Go to:", ["Upload File", "Data Summary", "Preprocessing", "Visualization"]
        )

        # Session state to store uploaded data
        if "uploaded_df" not in st.session_state:
            st.session_state.uploaded_df = None

        if page == "Upload File":
            self.upload_page.display()
        elif page == "Data Summary":
            self.summary_page.display()
        elif page == "Preprocessing":
            self.preprocessing_page.display()
        elif page == "Visualization":
            self.visualization_page.display()
