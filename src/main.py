import streamlit as st
import pandas as pd


# Function to validate and read the uploaded file
from services.data_validation import file_validation

# Streamlit App Title
st.title("📊 Sanitize The Data")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Upload File", "Data Summary", "Preprocessing", "Visualization"])

# Session state to store uploaded data
if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None

# File Upload Page
if page == "Upload File":
    
    uploaded_file = st.file_uploader("Upload CSV, Excel, or JSON", type=["csv", "xls", "xlsx", "json"])

    if uploaded_file:
        df = file_validation.validate_file_format(uploaded_file)  # Validate file
        
        if df is not None:
            st.session_state.uploaded_df = df  # Store only DataFrame
            st.dataframe(st.session_state.uploaded_df.head(10))  # Display data preview
        else:
            st.error("❌ Invalid file format or corrupted file. Please upload a valid CSV, Excel, or JSON.")

# Data Analysis Page (Placeholder)
elif page == "Data Summary":
    st.subheader("📊 Data Quality Analysis")
    if st.session_state.uploaded_df is not None:
        st.write("This section will include missing value detection, duplicates, and class imbalance checks.")
    else:
        st.warning("⚠ No file uploaded. Please upload a file first.")

# Preprocessing Page (Placeholder)
elif page == "Preprocessing":
    st.subheader("⚙ Data Preprocessing")
    if st.session_state.uploaded_df is not None:
        st.write("Options for missing value handling, scaling, and feature selection will be added here.")
    else:
        st.warning("⚠ No file uploaded. Please upload a file first.")

# Visualization Page (Placeholder)
elif page == "EDA":
    st.subheader("📈 Data Visualization")
    if st.session_state.uploaded_df is not None:
        st.write("Charts and graphs will be displayed here.")
    else:
        st.warning("⚠ No file uploaded. Please upload a file first.")



if __name__ == '__main__':
    print('SmartSanitize App Running...')