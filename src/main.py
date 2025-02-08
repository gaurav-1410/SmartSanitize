import streamlit as st
from presentation.ui import UIHandler
from presentation.visualization_page import VisualizationPage

# Streamlit App Title
st.title("📊 SmartSanitize - Data Cleaning App")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Upload File", "Data Summary", "Preprocessing", "Visualization"])

# Create an instance of UIHandler
ui = UIHandler()
visualization = VisualizationPage()

# File Upload Page
if page == "Upload File":
    ui.display_upload_page()

# Data Analysis Page
elif page == "Data Summary":
    ui.display_data_summary()

# Preprocessing Page
elif page == "Preprocessing":
    ui.display_preprocessing()

# Visualization Page
elif page == "Visualization":
    # ✅ Ensure uploaded_df exists before using it
    st.subheader("📊 Exploratory Data Analysis (EDA)")
    if "uploaded_df" in st.session_state and st.session_state.uploaded_df is not None:
        visualization.display_visualization_options(st.session_state.uploaded_df)
    else:
        st.warning("⚠ No data file uploaded. Please upload a file first.")

if __name__ == '__main__':
    print('SmartSanitize App Running...')
