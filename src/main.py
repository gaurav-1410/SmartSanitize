import streamlit as st
from presentation.navigation import Navigation


def main():
    """
    Entry point for the SmartSanitize App.
    """
    st.title("📊 Sanitize The Data")

    # Initialize Navigation
    nav = Navigation()
    nav.display_page()


if __name__ == "__main__":
    # print("SmartSanitize App Running...")
    main()
