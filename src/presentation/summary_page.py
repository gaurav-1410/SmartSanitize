import streamlit as st


class SummaryPage:
    """
    Displays Data Quality Analysis summary.
    """

    def display(self):
        st.subheader("📊 Data Quality Analysis")
        if st.session_state.uploaded_df is not None:
            st.write("This section will include missing value detection, duplicates, and class imbalance checks.")
        else:
            st.warning("⚠ No file uploaded. Please upload a file first.")
