import streamlit as st
import pandas as pd

class UploadPage:
    def __init__(self):
        pass
    
    def display_upload_page(self):
        """Handles file upload and stores the dataframe in session state"""
        st.subheader("📂 Upload Data File")

        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file, dtype=str)  # ✅ Load all columns as strings
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file, dtype=str)

                # ✅ Convert numeric columns back to proper types
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='ignore')

                # ✅ Store in session state
                st.session_state.uploaded_df = df

                st.success("✅ File uploaded successfully!")
                st.write(df.head())  # Show first 5 rows for preview

            except Exception as e:
                st.error(f"❌ Error loading file: {e}")

        if "uploaded_df" not in st.session_state:
            st.session_state.uploaded_df = None
