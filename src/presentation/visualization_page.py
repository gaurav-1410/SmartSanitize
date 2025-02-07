import streamlit as st


class VisualizationPage:
    """
    Handles data visualization.
    """

    def display(self):
        st.subheader("📈 Data Visualization")
        if st.session_state.uploaded_df is not None:
            st.write("Charts and graphs will be displayed here.")
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")
