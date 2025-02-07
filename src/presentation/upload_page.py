import streamlit as st
from infrastructure.file_loader import FileHandler


class UploadPage:
    """
    Handles file uploads and validation.
    """

    def __init__(self):
        self.file_handler = FileHandler()

    def display(self):
        """
        Renders the upload page UI.
        """
        self.file_handler.handle_file_upload()
