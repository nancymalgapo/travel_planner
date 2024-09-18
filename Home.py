import streamlit as st

from components.sidebar import app_sidebar


def main():
    app_sidebar()


if __name__ == "__main__":
    st.set_page_config(page_title="Your TravelMate", page_icon="🧳")
    main()
