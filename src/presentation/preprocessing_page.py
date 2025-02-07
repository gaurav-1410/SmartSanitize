import streamlit as st


class PreprocessingPage:
    """
    Handles data preprocessing options.
    """

    def display(self):
        st.subheader("⚙ Data Preprocessing")
        if st.session_state.uploaded_df is not None:
            st.write("Options for missing value handling, scaling, and feature selection will be added here.")
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")
