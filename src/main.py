import streamlit as st
from presentation.ui import UIHandler

# Streamlit App Title
st.title("📊 SmartSanitize - Data Cleaning App")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Upload File", "Data Summary", "Preprocessing", "Visualization"])

# Create an instance of UIHandler
ui = UIHandler()

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
    ui.display_visualization()

if __name__ == '__main__':
    print('SmartSanitize App Running...')
